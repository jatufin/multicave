from app import app
from flask import redirect, session, render_template, request, abort

import users
import messages
import messagefilter
import gameplay
import gameadmin
import errorhandlers

from db import db

@app.route("/")
def index():
    if _logged_in():
        user_id = session["user_id"]
        all_messages = messages.all_messages()
        public_games = gameplay.get_public_games()
        own_games = gameplay.get_games(user_id)
        current_rooms = gameplay.get_all_current_rooms(user_id)
        
        games = {"public_games": public_games,
                 "own_games" : own_games,
                 "current_rooms": current_rooms}
                 
        return render_template("index.html", messages=all_messages, games=games)

    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    _abort_if_invalid_form(request.form)

    username = request.form["username"]
    password = request.form["password"]

    if not users.login(username, password):
        return abort(403)

    return redirect("/")    

    
@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")


@app.route("/newuser")
def newuser():
    # _abort_if_not_logged_in(401)
    return render_template("newuser.html")

    
@app.route("/createuser", methods=["POST"])
def createuser():
    _abort_if_invalid_form(request.form)
    
    username = request.form["username"]
    password = request.form["password"]
    confirmpw = request.form["confirmpw"]

    if password != confirmpw:
        abort(401)

    users.createuser(username, password)

    if _is_admin():
        return redirect("/adminusers")

    return redirect("/")


@app.route("/message", methods=["POST"])
def message():
    ''' Write new message to the message board '''
    _abort_if_not_logged_in(401)
    _abort_if_invalid_form(request.form)
            
    body = request.form["body"]
    messages.new_message(body)
    
    return redirect("/")


@app.route("/playgame", methods=["POST"])
def playgame():
    _abort_if_not_logged_in(401)
    _abort_if_invalid_form(request.form)
    
    game_id = request.form["game_id"]
    user_id = session["user_id"]

    if "resetconfirm" in request.form:
        gameplay.reset_game(game_id=game_id, user_id=user_id)
        return redirect("/")
    
    if "gamereset" in request.form:
        return render_template("playgame.html", reset="YES", game_id=game_id)
    print("ROOM")
    if "target_room" not in request.form:
        room = gameplay.enter_current_room(game_id, user_id)
    else:
        room = gameplay.enter_room(game_id, user_id,
                                   request.form["target_room"])

    if not room:
        abort(404)
        
    return render_template("playgame.html", room=room)


@app.route("/adminusers")
def adminusers():
    _abort_if_not_admin()

    user_list = users.userlist()
    
    return render_template("adminusers.html", user_list=user_list)

@app.route("/updateuser", methods=["POST"])
def updateuser():
    _abort_if_not_admin()
    _abort_if_invalid_form(request.form)

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
    _abort_if_invalid_form(request.form)

    messagefilter.delete_and_add_words(form=request.form)

    return redirect("/bannedwords")

@app.route("/editgame")
def edit():
    ''' Edit your own adventure '''
    _abort_if_not_logged_in(401)
    _abort_if_invalid_form(request.form)

    user_id = session["user_id"]
    games = gameplay.get_games(user_id, create_if_not_found=True)

    # In future a user might own more than one game,
    # so using an array and selecting first
    game = gameadmin.get_game(games[0])
    
    return render_template("editgame.html", game=game)

@app.route("/updategame", methods=["POST"])
def updategame():
    _abort_if_not_logged_in(401)
    _abort_if_invalid_form(request.form)

    gameadmin.update_game(form=request.form)

    if "tag" in request.form:
        tag = request.form["tag"]
        
    return redirect(f"/editgame#{tag}")

           
@app.route("/newroom", methods=["POST"])
def newroom():
    _abort_if_not_logged_in(401)
    _abort_if_invalid_form(request.form)

    gameadmin.new_room(form=request.form)

    if "tag" in request.form:
        tag = request.form["tag"]
        
    return redirect(f"/editgame#{tag}")


@app.route("/updateroom", methods=["POST"])
def updateroom():
    _abort_if_not_logged_in(401)

    gameadmin.update_room(form=request.form)

    if "tag" in request.form:
        tag = request.form["tag"]
        
    return redirect(f"/editgame#{tag}")


@app.route("/deleteroom", methods=["POST"])
def deleteroom():
    _abort_if_not_logged_in(401)
    _abort_if_invalid_form(request.form)
    
    gameadmin.delete_room(form=request.form)

    return redirect("/editgame")

@app.route("/newcondition", methods=["POST"])
def newcondition():
    _abort_if_not_logged_in(401)
    _abort_if_invalid_form(request.form)

    gameadmin.new_condition(form=request.form)

    if "room_tag" in request.form:
        tag = request.form["room_tag"]
        
    return redirect(f"/editgame#{tag}")


@app.route("/updatecondition", methods=["POST"])
def updatecondition():
    _abort_if_not_logged_in(401)
    _abort_if_invalid_form(request.form)

    submit_action = request.form["submit_button"]

    if submit_action == "Update":
        gameadmin.update_condition(form=request.form)
    elif submit_action == "Delete":
        gameadmin.delete_condition(form=request.form)

    if "tag" in request.form:
        tag = request.form["tag"]
        
    return redirect(f"/editgame#{tag}")        


@app.route("/newconditionroom", methods=["POST"])
def newconditionroom():
    _abort_if_not_logged_in(401)
    _abort_if_invalid_form(request.form)

    gameadmin.new_conditionroom(form=request.form)

    if "room_tag" in request.form:
        tag = request.form["room_tag"]
        
    return redirect(f"/editgame#{tag}")


@app.route("/removeconditionroom", methods=["POST"])
def removeconditionroom():
    _abort_if_not_logged_in(401)
    _abort_if_invalid_form(request.form)

    gameadmin.remove_conditionroom(form=request.form)

    if "room_tag" in request.form:
        tag = request.form["room_tag"]
        
    return redirect(f"/editgame#{tag}")


def _logged_in():
    if "logged_in" not in session:
        return False
    return True


def _abort_if_not_logged_in(code):
    if not _logged_in():
        abort(code)

        
def _abort_if_not_admin():
    if not _is_admin():
        abort(401)

        
def _is_admin():
    return "adm" in session and session["adm"]


def _abort_if_invalid_form(form):
    if _fields_too_long(form):
        abort(413)

        
def _fields_too_long(form):
    """ Goes over all fields in a form, and returns False if one exceeds
    the limit value
    """
    limit = 1000  # Limit value for a length in any field
    for name, value in form.items():
        print(f"Name: {name} Pituus: {len(value)}")
        if len(value) > limit:
            return True
    
    return False

    
    
