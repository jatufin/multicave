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
    """Main page
    """
    all_messages = messages.all_messages()
    
    public_games = gameplay.get_public_games()
    games = {"public_games": public_games}
    
    if _logged_in():
        user_id = session["user_id"]
        
        own_games = gameplay.get_games(user_id)
        current_rooms = gameplay.get_all_current_rooms(user_id)
        
        games["own_games"] =  own_games,
        games["current_rooms"] : current_rooms

    return render_template("index.html", messages=all_messages, games=games)



@app.route("/login", methods=["POST"])
def login():
    """Receive and process the login form
    """
    _abort_if_invalid_form(request.form)

    username = request.form["username"]
    password = request.form["password"]

    if not users.login(username, password):
        return abort(403)

    return redirect("/")    

    
@app.route("/logout")
def logout():
    """Execute logout rutines, which clear the session and
    redirect to main page
    """
    users.logout()
    return redirect("/")


@app.route("/newuser")
def newuser():
    """Open the form for creating a new user
    """

    return render_template("newuser.html")

    
@app.route("/createuser", methods=["POST"])
def createuser():
    """Receive and process the new user form
    """
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

@app.route("/help")
def help():
    """Open the help page
    """
    _abort_if_not_logged_in(403)

    return render_template("help.html")

@app.route("/pwreset")
def pwreset():
    """Open the password reset page
    """
    _abort_if_not_logged_in(403)

    return render_template("pwreset.html")


@app.route("/changepw", methods=["POST"])
def changepw():
    """Receive and process the password reset form
    """
    _abort_if_not_logged_in(403)
    _abort_if_invalid_form(request.form)

    username = session["username"]
    
    oldpassword = request.form["oldpassword"]
    password = request.form["password"]
    confirmpw = request.form["confirmpw"]

    if password != confirmpw:
        abort(401)

    if not users.change_password(username, oldpassword, password):
        abort(403)

    if _is_admin():
        return redirect("/adminusers")

    return redirect("/")

    
@app.route("/message", methods=["POST"])
def message():
    """Receive and process the password reset form
    """
    _abort_if_not_logged_in(401)
    _abort_if_invalid_form(request.form)
            
    body = request.form["body"]
    messages.new_message(body)
    
    return redirect("/")


@app.route("/playgame", methods=["POST"])
def playgame():
    """Receive and process the form opening a game for playing
    """    
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
    """Open the page for user administration
    """
    _abort_if_not_admin()

    user_list = users.userlist()
    
    return render_template("adminusers.html", user_list=user_list)

@app.route("/updateuser", methods=["POST"])
def updateuser():
    """Receive and process the form updating user account infromation
    """
    _abort_if_not_admin()
    _abort_if_invalid_form(request.form)

    users.updateuser(form=request.form)

    return redirect("/adminusers")

@app.route("/bannedwords")
def bannedwords():
    """Open the page for message filter administration
    """    
    _abort_if_not_admin()

    word_list = messagefilter.all_words()

    return render_template("bannedwords.html", word_list=word_list)

@app.route("/updatewords", methods=["POST"])
def updatewords():
    """Receive and process the form updating message filter
    """    
    _abort_if_not_admin()
    _abort_if_invalid_form(request.form)

    messagefilter.delete_and_add_words(form=request.form)

    return redirect("/bannedwords")

@app.route("/editgame")
def edit():
    """Open the page for game editing
    """    
    _abort_if_not_logged_in(401)
    # _abort_if_invalid_form(request.form)

    user_id = session["user_id"]
    games = gameplay.get_games(user_id, create_if_not_found=True)

    # In future a user might own more than one game,
    # so using an array and selecting first
    game = gameadmin.get_game(games[0])
    
    return render_template("editgame.html", game=game)

@app.route("/updategame", methods=["POST"])
def updategame():
    """Receive and process the form for editing and updating a game
    """  
    _abort_if_not_logged_in(401)
    _abort_if_invalid_form(request.form)

    gameadmin.update_game(form=request.form)

    tag = _get_room_tag(request.form)                            
        
    return redirect(f"/editgame#{tag}")

           
@app.route("/newroom", methods=["POST"])
def newroom():
    """Receive and process the form for creating of a new room to a game
    """    
    _abort_if_not_logged_in(401)
    _abort_if_invalid_form(request.form)

    gameadmin.new_room(form=request.form)

    tag = _get_room_tag(request.form)                        
        
    return redirect(f"/editgame#{tag}")


@app.route("/updateroom", methods=["POST"])
def updateroom():
    """Receive and process the form for updating a room to a game
    """    
    _abort_if_not_logged_in(401)

    gameadmin.update_room(form=request.form)

    tag = _get_room_tag(request.form)                    
        
    return redirect(f"/editgame#{tag}")


@app.route("/deleteroom", methods=["POST"])
def deleteroom():
    """Receive and process the form for deleting a room from a game
    """    
    _abort_if_not_logged_in(401)
    _abort_if_invalid_form(request.form)
    
    gameadmin.delete_room(form=request.form)

    return redirect("/editgame")

@app.route("/newcondition", methods=["POST"])
def newcondition():
    """Receive and process the form for creating of a new condition
    to a room in a game
    """  
    _abort_if_not_logged_in(401)
    _abort_if_invalid_form(request.form)

    gameadmin.new_condition(form=request.form)

    tag = _get_room_tag(request.form)                
        
    return redirect(f"/editgame#{tag}")


@app.route("/updatecondition", methods=["POST"])
def updatecondition():
    """Receive and process the form for updating of a condition in a game
    """        
    _abort_if_not_logged_in(401)
    _abort_if_invalid_form(request.form)

    submit_action = request.form["submit_button"]

    if submit_action == "Update":
        gameadmin.update_condition(form=request.form)
    elif submit_action == "Delete":
        gameadmin.delete_condition(form=request.form)

    tag = _get_room_tag(request.form)            
        
    return redirect(f"/editgame#{tag}")        


@app.route("/newconditionroom", methods=["POST"])
def newconditionroom():
    """Receive and process the form for adding a room to a condition
    """    
    _abort_if_not_logged_in(401)
    _abort_if_invalid_form(request.form)

    gameadmin.new_conditionroom(form=request.form)

    tag = _get_room_tag(request.form)    
        
    return redirect(f"/editgame#{tag}")


@app.route("/removeconditionroom", methods=["POST"])
def removeconditionroom():
    """Receive and process the form for removing a room from a condition
    """        
    _abort_if_not_logged_in(401)
    _abort_if_invalid_form(request.form)

    gameadmin.remove_conditionroom(form=request.form)

    tag = _get_room_tag(request.form)
        
    return redirect(f"/editgame#{tag}")


def _logged_in():
    """Check if a session is active
    """
    if "logged_in" not in session:
        return False
    return True


def _abort_if_not_logged_in(code):
    """Abort request, if user is not logged in

    Args:
        code : Integer used as HTTP code.
    """
    if not _logged_in():
        abort(code)

        
def _abort_if_not_admin():
    """Abort request, if logged in user has no administrative rights
    """    
    if not _is_admin():
        abort(401)

        
def _is_admin():
    """Check if the current user has admin rights

    Returns:
        Boolean
    """
    return "adm" in session and session["adm"]


def _abort_if_invalid_form(form):
    """Check if the sent form is valid for input

    Args:
        form : HTML form

    Returns:
        Boolean
    """    
    if _logged_in():
        form_token = form["csrf_token"]
        session_token = session["csrf_token"]
        if form_token != session_token:
            abort(403)
        
    if _fields_too_long(form):
        abort(413)

        
def _get_room_tag(form):
    """Extract room tag from the form

    Args:
        form : HTML form

    Returns:
        String containing the tag, or empty string if tag can't be found.
    """
    if "room_tag" in form:
        tag = form["room_tag"]
    else:
        tag = ""

    return tag


def _fields_too_long(form):
    """ Goes over all fields in a form, and returns False if one exceeds
    the limit value

    Args:
        form : HTML form

    Returns:
        Boolean
    """
    limit = 1000  # Limit value for a length in any field
    for name, value in form.items():
        print(f"Name: {name} Pituus: {len(value)}")
        if len(value) > limit:
            return True
    
    return False

    
    
