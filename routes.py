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
    if not session["logged_in"]:
        abort(401)
    return render_template("newuser.html")

@app.route("/message", methods=["POST"])
def message():
    ''' Write new message to the message board '''
    if not session["logged_in"]:
        abort(401) 
    body = request.form["body"]
    messages.new_message(body)
    
    return redirect("/")

@app.route("/createuser", methods=["POST"])
def createuser():
    if not session["logged_in"]:
        abort(401)
    username = request.form["username"]
    password = request.form["password"]
    confirmpw = request.form["confirmpw"]

    if password != confirmpw:
        abort(401)

    users.createuser(username, password)
    
    return redirect("/")


@app.route("/edit")
def edit():
    ''' Edit your own adventure '''
    if not session["logged_in"]:
        abort(401)

    rooms = dungeon.all_rooms(session["user_id"])

    return render_template("edit.html", rooms=rooms)

@app.route("/newroom", methods=["POST"])
def newroom():
    if not session["logged_in"]:
        abort(401)

    dungeon.create_room(session["user_id"], form=request.form)
    return redirect("/edit")


    
