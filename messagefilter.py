from flask import abort
from db import db


def all_words():
    """Return all words in the ban list

    Returns:
        A list of strings
    """
    sql = "SELECT word FROM banned_words ORDER BY word"
    result = db.session.execute(sql)
    word_list = result.fetchall()

    return word_list


def delete_and_add_words(form):
    """Handle the form, which can delete and add new words to the list

    Args:
        form : HTML form dictionary from route
    """
    words = form.getlist("banned")

    for word in words:
        _delete_word(word)
    
    new_words = form["new_words"].split()

    for word in new_words:
        _add_word(word)


def contains_banned(text):
    """Checks if the given text contains any of the banned words

    Args:
        text : String

    Returns:
        Boolean
    """
    sql = "SELECT word FROM banned_words;"
    words = db.session.execute(sql)
    text = text.lower()
    
    for word in words:
        if word.word in text:
            return True

    return False

    
def _delete_word(word):
    """Delete a word from the banned words list

    Args:
        word : String.
    """
    sql = "DELETE FROM banned_words WHERE word=:word"

    try:
        db.session.execute(sql, {"word": word})
        db.session.commit()
    except:
        abort(404)

        
def _add_word(word):
    """Add a word to the banned words list

    Args:
        word : String.
    """    
    sql = "INSERT INTO banned_words (word) VALUES (:word)"
    try:
        db.session.execute(sql, {"word": word.lower()})
        db.session.commit()
    except:
        abort(401)
