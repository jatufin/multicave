from flask import render_template
from app import app


@app.errorhandler(401)
def unauthorized_error(error):
    ''' HTTP 401: Bad request
    '''
    return render_template("error.html", message="401: You are not a member of the cult!")


@app.errorhandler(403)
def forbidden_error(error):
    ''' HTTP 403: Forbidden
    '''
    return render_template("error.html", message="403: Forbidden")


@app.errorhandler(404)
def notfound_error(error):
    ''' HTTP 404: Not found
    '''
    return render_template("error.html", message="404: Not found")


@app.errorhandler(409)
def conflict_error(error):
    ''' HTTP 409: Conflict
    '''
    return render_template("error.html", message="409: Bad name")


@app.errorhandler(413)
def payloadtoolarge_error(error):
    ''' HTTP 413: Payload Too Large
    '''
    return render_template("error.html", message="413: Payload Too Large")
                        
