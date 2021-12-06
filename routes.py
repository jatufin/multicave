from app import app
from flask import redirect, session, render_template, request, abort

import users
import messages
import messagefilter
import gameadmin
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

@app.route("/bannedwords")
def bannedwords():
    _abort_if_not_admin()

    word_list = messagefilter.all_words()

    return render_template("bannedwords.html", word_list=word_list)

@app.route("/updatewords", methods=["POST"])
def updatewords():
    _abort_if_not_admin()

    messagefilter.delete_and_add_words(form=request.form)

    return redirect("/bannedwords")

@app.route("/editgame")
def edit():
    ''' Edit your own adventure '''
    _abort_if_not_logged_in(401)            

    user_id = session["user_id"]
    games = gameadmin.get_games(user_id, create_if_not_found=True)

    return render_template("editgame.html", game=games[0])

@app.route("/updategame", methods=["POST"])
def updategame():

    return render_template("/editgame")

           
@app.route("/newroom", methods=["POST"])
def newroom():
    _abort_if_not_logged_in(401)                

    dungeon.create_room(session["user_id"], form=request.form)
    return redirect("/editgame")


def _abort_if_not_logged_in(code):
    if not "logged_in" in session:
        abort(code)

def _abort_if_not_admin():
    if not _is_admin():
        abort(401)

def _is_admin():
    return "adm" in session and session["adm"]
