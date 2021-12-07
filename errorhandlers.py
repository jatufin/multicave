from flask import render_template
from app import app

@app.errorhandler(401)
def unauthorized_error(error):
    return render_template("error.html", message="401: You are not a member of the cult!")

@app.errorhandler(404)
def unauthorized_error(error):
    return render_template("error.html", message="404: Not found")

@app.errorhandler(409)
def unauthorized_error(error):
    return render_template("error.html", message="409: Bad name")
                        
