from app import app
from flask import redirect, session, render_template, request, abort

import users
import messages
import dungeon
import errorhandlers

from db import db

@app.route("/")
def index():
    all_messages = messages.all_messages()
    
    return render_template("index.html", messages=all_messages)

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    if users.login(username, password):
        return redirect("/")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")


@app.route("/newuser")
def newuser():
    # _abort_if_not_logged_in(401)
    return render_template("newuser.html")

@app.route("/message", methods=["POST"])
def message():
    ''' Write new message to the message board '''
    _abort_if_not_logged_in(401)
    body = request.form["body"]
    messages.new_message(body)
    
    return redirect("/")

@app.route("/createuser", methods=["POST"])
def createuser():
    # _abort_if_not_logged_in(401)    

    username = request.form["username"]
    password = request.form["password"]
    confirmpw = request.form["confirmpw"]

    if password != confirmpw:
        abort(401)

    users.createuser(username, password)

    if _is_admin():
        return redirect("/adminusers")

    return redirect("/")

@app.route("/adminusers")
def adminusers():
    _abort_if_not_admin()

    user_list = users.userlist()
    
    return render_template("adminusers.html", user_list=user_list)

@app.route("/updateuser", methods=["POST"])
def updateuser():
    _abort_if_not_admin()

    users.updateuser(form=request.form)

    return redirect("/adminusers")
    
@app.route("/edit")
def edit():
    ''' Edit your own adventure '''
    _abort_if_not_logged_in(401)            

    rooms = dungeon.all_rooms(session["user_id"])

    return render_template("edit.html", rooms=rooms)

@app.route("/newroom", methods=["POST"])
def newroom():
    _abort_if_not_logged_in(401)                

    dungeon.create_room(session["user_id"], form=request.form)
    return redirect("/edit")


def _abort_if_not_logged_in(code):
    if not "logged_in" in session:
        abort(code)

def _abort_if_not_admin():
    if not session["admin"]:
        abort(401)

def _is_admin():
    return session["admin"]
