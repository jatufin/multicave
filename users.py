from flask import session, abort
from db import db

from werkzeug.security import check_password_hash, generate_password_hash


def login(username, password):
    sql = "SELECT id, locked, password, admin, public FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if not user:
        abort(401)

    if user.locked:
        abort(401)

    hash_value = user.password
    if not check_password_hash(hash_value, password):
        abort(401)

    session["logged_in"] = True
    session["username"] = username
    session["user_id"] = user.id
    session["admin"] = user.admin
    session["public"] = user.public
    
    return True
            

def createuser(username, password):    
                                
    sql = "INSERT INTO users (username) VALUES (:username)"

    try:
        db.session.execute(sql, {"username": username})
        db.session.commit()
    except:
        abort(409)

    set_password(username, password)
                             
def userlist():
    sql = "SELECT id, locked, admin, public, username FROM users ORDER BY id"
    result = db.session.execute(sql)
    users = result.fetchall()

    return users

def updateuser(form):
    username = form["username"]

    if form.get("delete_selection"):
        return deleteuser(username)
    
    admin = "True" if form.get("admin_selection") else "False"
    locked = "True" if form.get("locked_selection") else "False"
    public = "True" if form.get("public_selection") else "False"   
    
    sql = "UPDATE users SET admin=:admin, locked=:locked, public=:public WHERE username=:username"
    try:
        print("Foo")
        db.session.execute(sql, {"username": username,
                                 "admin": admin,
                                 "locked": locked,
                                 "public": public})
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
    _clear_session("admin")
    _clear_session("public")

def _clear_session(property):
    if property in session:
        del session[property]
    
