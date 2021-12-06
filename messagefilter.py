from flask import abort
from db import db


def all_words():
    sql = "SELECT word FROM banned_words ORDER BY word"
    result = db.session.execute(sql)
    word_list = result.fetchall()

    return word_list


def delete_and_add_words(form):
    words = form.getlist("banned")

    for word in words:
        _delete_word(word)
    
    new_words = form["new_words"].split()

    for word in new_words:
        _add_word(word)


def contains_banned(text):
    sql = "SELECT word FROM banned_words;"
    words = db.session.execute(sql)
    text = text.lower()
    
    for word in words:
        if word.word in text:
            return True

    return False

    
def _delete_word(word):
    sql = "DELETE FROM banned_words WHERE word=:word"

    try:
        db.session.execute(sql, {"word": word})
        db.session.commit()
    except:
        abort(404)

        
def _add_word(word):
    sql = "INSERT INTO banned_words (word) VALUES (:word)"
    try:
        db.session.execute(sql, {"word": word.lower()})
        db.session.commit()
    except:
        abort(401)
