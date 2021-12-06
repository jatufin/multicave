from flask import session, abort
from db import db

def get_public_games(): # TODI: Check if the user is marked it as public
    sql = "SELECT * FROM games WHERE published='t'"
    result = db.session(sql)
    games = result.fetchall()
    
    return games
    
def get_games(user_id, create_if_not_found=False):
    sql = "SELECT * FROM games WHERE owner_id=:owner_id"
    result = db.session.execute(sql, {"owner_id": user_id})
    games = result.fetchall()
    
    if not games and create_if_not_found:
        create_game(user_id)
        return get_games(user_id)

    return games

def get_rooms(game_id):
    sql = "SELECT * FROM rooms WHERE game_id=:game_id"
    result = db.session.execute(sql, {"game_id": game_id})
    rooms = result.fetchall()

    return rooms

def get_conditions(game_id):
    sql = "SELECT * FROM conditions WHERE game_id=:game_id"
    result = db.session.execute(sql, {"game_id": game_id})
    conditions = result.fetchall()

    return conditions

def get_condition_rooms(game_id):
    sql = "SELECT * FROM condition_rooms WHERE game_id=:game_id"
    result = db.session.execute(sql, {"game_id": game_id})
    condition_rooms = result.fetchall()

    return condition_rooms

def create_game(user_id):
    sql = "INSERT INTO games (owner_id) VALUES (:owner_id)"
    try:
        db.session.execute(sql, {"owner_id": user_id})
        db.session.commit()
    except:
        abort(401)
