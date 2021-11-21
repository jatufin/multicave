from flask import Flask
from flask import abort
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import check_password_hash, generate_password_hash

from os import getenv

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

# For local database
# app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
# For Heroku
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


@app.route("/")
def index():
    sql = "SELECT users.username, messages.posting_date, messages.body FROM messages INNER JOIN users on messages.user_id = users.id"
    result = db.session.execute(sql)
    messages = result.fetchall()
    
    return render_template("index.html", messages=messages)

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        abort(401)
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session["username"] = username
            session["user_id"] = user.id
            return redirect("/")
        else:
            abort(401)

@app.route("/message", methods=["POST"])
def message():
    ''' Write new message to the message board '''
    body = request.form["body"]
    user_id = session["user_id"]
    
    sql = "INSERT INTO messages (user_id, body) VALUES (:user_id, :body)"
    try:
        db.session.execute(sql, {"user_id":user_id, "body":body})
        db.session.commit()
    except:
        abort(401)

    return redirect("/")
        
@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/newuser")
def newuser():
    return render_template("newuser.html")

@app.route("/createuser", methods=["POST"])
def createuser():
    username = request.form["username"]
    password = request.form["password"]
    confirmpw = request.form["confirmpw"]

    if password != confirmpw:
        abort(401)
    
    hash_value = generate_password_hash(password)
                                
    sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
    try:
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
    except:
        abort(409)
        
    return redirect("/")

@app.route("/edit")
def edit():
    ''' Edit your own adventure '''
    if not "username" in session:
        abort(401)

    user_id = session["user_id"]
    username = session["username"]

    sql = "SELECT * FROM dungeons WHERE user_id=:user_id"
    result = db.session.execute(sql, {"user_id":user_id})
    rooms = result.fetchall()
    
    return render_template("edit.html", rooms=rooms)

@app.route("/newroom", methods=["POST"])
def newroom():
    if not "username" in session:
        abort(401)
    user_id = session["user_id"]
    sql = '''
    INSERT INTO dungeons (
       tag,
       user_id,
       description,
       north_choice,
       north_target,
       south_choice,
       south_target,
       east_choice,
       east_target,
       west_choice,
       west_target
    ) VALUES (
       :tag,
       :user_id,
       :description,
       :north_choice,
       :north_target,
       :south_choice,
       :south_target,
       :east_choice,
       :east_target,
       :west_choice,
       :west_target
    )
    '''
    values = {
        "tag":request.form["tag"],
        "user_id":user_id,
        "description":request.form["description"],
        "north_choice":request.form["north_choice"],
        "north_target":request.form["north_target"],
        "south_choice":request.form["south_choice"],
        "south_target":request.form["south_target"],
        "east_choice":request.form["east_choice"],
        "east_target":request.form["east_target"],
        "west_choice":request.form["west_choice"],
        "west_target":request.form["west_target"]
    }
    #try:
    db.session.execute(sql, values)
    db.session.commit()
    #except:
    #    abort(409)
    return redirect("/edit")
    
@app.errorhandler(401)
def unauthorized_error(error):
    return render_template("error.html", message="401: You are not a member of the cult!")
                        
@app.errorhandler(409)
def unauthorized_error(error):
    return render_template("error.html", message="409: Bad name")
                        
