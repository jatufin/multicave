from flask import session, abort
from db import db

def get_public_games(): # TODI: Check if the user is marked it as public
    sql = "SELECT * FROM games WHERE published='t'"
    result = db.session.execute(sql)
    games = result.fetchall()
    
    return games


def get_games(user_id, create_if_not_found=False):
    sql = "SELECT * FROM games WHERE owner_id=:user_id"
    result = db.session.execute(sql, {"user_id": user_id})
    games = result.fetchall()
    
    if not games and create_if_not_found:
        create_game(user_id)
        return get_games(user_id)

    return games


def get_all_current_rooms(user_id):
    sql = "SELECT * FROM current_rooms WHERE player_id=:user_id"
    result = db.session.execute(sql, {"user_id": user_id})
    current_rooms = result.fetchall()

    return current_rooms


def get_current_room(game_id, user_id):
    """ First looku up the current_room tables if the user has not
    room for this game there, look up for the start_room of the game
    """
    sql = "SELECT room_tag FROM current_rooms WHERE player_id=:user_id AND game_id=:game_id"
    result = db.session.execute(sql, {"user_id": user_id, "game_id": game_id})
    rooms = result.fetchall()

    if not rooms:
        sql = "SELECT start_room FROM games WHERE id=:game_id"
        result = db.session.execute(sql, {"game_id": game_id})
        rooms = result.fetchall()
        if not rooms:
            abort(405)
        else:
            room_tag = rooms[0].start_room
    else:
        room_tag = rooms[0].room_tag
    
    return room_tag


def enter_current_room(game_id, user_id):
    current_room = get_current_room(game_id, user_id)

    return enter_room(game_id, user_id, current_room)

    

def enter_room(game_id, user_id, room_tag):
    """ First check, if user is allowed to enter the room.
    If user has not visited the room before, visited_rooms table is updated, and return description is
    constructed based on if this is first visit or not.

    Possible choices are returned as a list of descriptions and tags of the target rooms.

    Return value can be used by playgame.html template, to render the room.
    """
    
    if not can_enter(game_id, user_id, room_tag):
        return None

    if has_visited(game_id, user_id, room_tag):
        sql = "SELECT title, description, next_visits_description AS more_text FROM rooms WHERE game_id=:game_id AND tag=:room_tag"
    else:
        sql = "SELECT title, description, first_visit_description AS more_text FROM rooms WHERE game_id=:game_id AND tag=:room_tag"
        mark_as_visited(game_id, user_id, room_tag)
        
    result = db.session.execute(sql, {"game_id": game_id, "room_tag": room_tag})
    # result = db.session.execute(sql, {"game_id": 1, "room_tag": "A"})
    room_texts = result.fetchall()

    if not room_texts:
        return_object = {"title": "<not found>",
                         "description": "<not found>"}
    else:
        return_object = {"title": room_texts[0].title,
                         "description": room_texts[0].description + "\n\n" + room_texts[0].more_text}
    
    return return_object


def all_visited_rooms(game_id, user_id):
    sql = "SELECT room_tag FROM visited_rooms WHERE game_id=:game_id AND player_id=:user_id"
    result = db.session.execute(sql, {"user_id": user_id, "game_id": game_id})
    visited_rooms = result.fetchall()

    return visited_rooms

def has_visited(game_id, user_id, room_tag):
    sql = "SELECT room_tag FROM visited_rooms WHERE game_id=:game_id AND player_id=:user_id AND room_tag=:room_tag"
    result = db.session.execute(sql, {"user_id": user_id,
                                      "game_id": game_id,
                                      "room_tag": room_tag})
    rooms = result.fetchall()

    return True if rooms else False


def is_startroom(game_id, room_tag):
    sql = "SELECT start_room FROM games WHERE id=:game_id"
    result = db.session.execute(sql, {"game_id": game_id})
    start_room = result.fetchone().start_room

    return True if start_room == room_tag else False
    
    
def can_enter(game_id, user_id, room_tag):
    if is_startroom(game_id, room_tag):
        return True

    return True  # TODO: proper checks for target validity


def mark_as_visited(game_id, user_id, room_tag):
    sql = "INSERT INTO visited_rooms (game_id, room_tag, player_id) VALUES (:game_id, :room_tag, :player_id)"
    try:
        db.session.execute(sql, {"game_id": game_id,
                                 "room_tag": room_tag,
                                 "player_id": user_id})
        db.session.commit()
    except:
        abort(409)
