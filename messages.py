from flask import session, abort
from db import db

import messagefilter

def all_messages():
    ''' Get all messages from the messages table
    '''
    sql = "SELECT users.username, messages.posting_date, messages.body FROM messages INNER JOIN users on messages.user_id = users.id"
    result = db.session.execute(sql)
    messages = result.fetchall()

    return messages

def new_message(body):
    ''' Add new message to the messages table
    '''
    user_id = session["user_id"]

    if not is_valid_message(body):
        abort(409)
    
    sql = "INSERT INTO messages (user_id, body) VALUES (:user_id, :body)"
    try:
        db.session.execute(sql, {"user_id":user_id, "body":body})
        db.session.commit()
    except:
        abort(401)

def is_valid_message(text):
    ''' Validate the new message is not empty, and does not cotain
    banned words
    '''
    if not text:
        return False

    if messagefilter.contains_banned(text):
        return False

    return True
