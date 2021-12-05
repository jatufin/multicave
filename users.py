from flask import session, abort
from db import db

from werkzeug.security import check_password_hash, generate_password_hash


def login(username, password):
    sql = "SELECT id, password, admin, public FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if not user:
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
    hash_value = generate_password_hash(password)
                                
    sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
    try:
        db.session.execute(sql, {"username": username, "password": hash_value})
        db.session.commit()
    except:
        abort(409)

def logout():
    session["logged_in"] = False
    del session["username"]
    del session["user_id"]
    del session["admin"]
    del session["public"]
    
