from flask import session, abort
from db import db
import random

from werkzeug.security import check_password_hash, generate_password_hash


def login(username, password):
    sql = "SELECT id, locked, password, adm FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()

    if not user:
        return False

    if user.locked:
        return False

    hash_value = user.password
    if not check_password_hash(hash_value, password):
        return False

    session["logged_in"] = True
    session["username"] = username
    session["user_id"] = user.id
    session["adm"] = user.adm
    
    return True
            

def createuser(username, password):
    """Create new user into the users table

    Args:
        username : String
        password : String
    """
    sql = "INSERT INTO users (username, password) VALUES (:username, :password)"

    # The value is mandatory, so fill it with a random string
    dummy_password = ''.join(random.SystemRandom().choice("1234567890") for _ in range(100))
    
    try:
        db.session.execute(sql, {"username": username,
                                 "password": dummy_password})
        db.session.commit()
    except:
        abort(409)

    # Properly create a password hash
    set_password(username, password)
                             
def userlist():
    sql = "SELECT id, locked, adm, username FROM users ORDER BY id"
    result = db.session.execute(sql)
    users = result.fetchall()

    return users

def updateuser(form):
    username = form["username"]

    if form.get("delete_selection"):
        return deleteuser(username)
    
    adm = "True" if form.get("adm_selection") else "False"
    locked = "True" if form.get("locked_selection") else "False"

    sql = "UPDATE users SET adm=:adm, locked=:locked WHERE username=:username"
    try:
        db.session.execute(sql, {"username": username,
                                 "adm": adm,
                                 "locked": locked})
        db.session.commit()
    except:
        abort(409)

    password = form["password"]
    confirmpw = form["confirmpw"]

    if password and password == confirmpw:
        set_password(username, password)

def set_password(username, password):
    sql = "UPDATE users SET password=:password WHERE username=:username"
    hash_value = generate_password_hash(password)
    
    try:
        db.session.execute(sql, {"username": username, "password": hash_value})
        db.session.commit()
    except:
        abort(409)

def change_password(username, oldpassword, password):
    sql = "SELECT password, locked FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()

    if not user:
        return False

    if user.locked:
        return False

    hash_value = user.password
    if not check_password_hash(hash_value, oldpassword):
        return False

    set_password(username, password)
    return True
    
def deleteuser(username):
    sql = "DELETE FROM users WHERE username=:username"
    try:
        db.session.execute(sql, {"username": username})
        db.session.commit()
    except:
        abort(401)
    
    
def logout():
    _clear_session("logged_in")
    _clear_session("username")
    _clear_session("locked")
    _clear_session("user_id")
    _clear_session("adm")

def _clear_session(property):
    if property in session:
        del session[property]
    
