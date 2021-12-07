from flask import session, abort
from db import db

import gameadmin

def get_public_games(): # TODI: Check if the user is marked it as public
    sql = "SELECT * FROM games WHERE published='t'"
    result = db.session.execute(sql)
    games = result.fetchall()
    
    return games


def get_games(user_id, create_if_not_found=False):
    ''' Get list of all the games user is owner of.
    Currently each user has only one own game.
    '''
    sql = "SELECT * FROM games WHERE owner_id=:user_id"
    result = db.session.execute(sql, {"user_id": user_id})
    games = result.fetchall()
    
    if not games and create_if_not_found:
        create_game(user_id)
        return get_games(user_id)

    return games


def get_all_current_rooms(user_id):
    ''' Get list of all rooms in all games where user currently is
    '''
    sql = "SELECT * FROM current_rooms WHERE player_id=:user_id"
    result = db.session.execute(sql, {"user_id": user_id})
    current_rooms = result.fetchall()

    return current_rooms


def get_current_room(game_id, user_id):
    """ First look up the current_room tables if the user has not
    room for this game there, look up for the start_room of the game
    and add it to the current_rooms table for the user
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
            insert_current_room(game_id, user_id, room_tag)
    else:
        room_tag = rooms[0].room_tag
    
    return room_tag


def enter_current_room(game_id, user_id):
    ''' Go to the room, which has been saved to the current_rooms table,
    otherwise the starting room of the game will be opened.
    '''
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

    update_current_room(game_id, user_id, room_tag)
    
    if has_visited(game_id, user_id, room_tag):
        sql = "SELECT title, description, next_visits_description AS more_text FROM rooms WHERE game_id=:game_id AND tag=:room_tag"
    else:
        sql = "SELECT title, description, first_visit_description AS more_text FROM rooms WHERE game_id=:game_id AND tag=:room_tag"
        mark_as_visited(game_id, user_id, room_tag)
    
    result = db.session.execute(sql, {"game_id": game_id, "room_tag": room_tag})
    room_texts = result.fetchall()

    return_object = {"game_id": game_id}
    if not room_texts:
        return_object["title"] = "<not found>",
        return_object["descriptions"] = ["<not found>"]
    else:
        return_object["title"] = room_texts[0].title
        return_object["descriptions"] = [room_texts[0].description, room_texts[0].more_text]
        

    conditions = get_condition_results(game_id, user_id)

    # Add list of descriptions based on visited rooms
    return_object["descriptions"] = conditions["descriptions"]
    
    # List of possible choices user can make
    return_object["choices"] = conditions["choices"]

    return return_object


def all_visited_rooms(game_id, user_id):
    ''' Return list of all rooms user has visited in this game
    '''
    sql = "SELECT room_tag FROM visited_rooms WHERE game_id=:game_id AND player_id=:user_id"
    result = db.session.execute(sql, {"user_id": user_id, "game_id": game_id})
    visited_rooms = result.fetchall()

    return visited_rooms

def has_visited(game_id, user_id, room_tag):
    ''' Check if the user has aleready visited in this room
    '''
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
    
def get_condition_results(game_id, user_id):
    ''' Compare visited_rooms table to the the requirements of the conditions
    and based on them return description text for the room and list of
    choices user can make in this room
    '''
    current_room = get_current_room(game_id, user_id)

    sql = "SELECT * FROM conditions WHERE game_id=:game_id AND room_tag=:current_room"
    result = db.session.execute(sql, {"game_id": game_id,
                                      "current_room": current_room})
    conditions = result.fetchall()

    visited_rooms = all_visited_rooms(game_id, user_id)

    descriptions = []
    choices = []

    for condition in conditions:
        sql = "SELECT * FROM condition_rooms WHERE condition_id=:condition_id"
        result = db.session.execute(sql, {"condition_id": condition.id})
        condition_rooms = result.fetchall()
       
        all_condition_rooms_visited = True

        for room in condition_rooms:
            if room not in visited_rooms:
                condition = False
                
        if all_condition_rooms_visited:
            descriptions.append(condition.all_visited)
            choices.append({"choice": condition.all_visited_choice,
                            "target_room": condition.all_visited_target})
        else:
            descriptions.append(condition.not_all_visited)
                    
    return {"descriptions": descriptions,
            "choices": choices}
    
    
def can_enter(game_id, user_id, room_tag):
    ''' Check if user is allowed to enter to the particular room
    ''' 
    if is_startroom(game_id, room_tag):
        return True

    if room_tag == get_current_room(game_id, user_id):
        return True
    
    conditions = get_condition_results(game_id, user_id)
    for choice in conditions["choices"]:
        if choice["target_room"] == room_tag:
            return True
        
    return False


def mark_as_visited(game_id, user_id, room_tag):
    ''' As user enters first time to a room, the room is added to the visited
    rooms of the user in this particular game
    '''
    sql = "INSERT INTO visited_rooms (game_id, room_tag, player_id) VALUES (:game_id, :room_tag, :player_id)"
    try:
        db.session.execute(sql, {"game_id": game_id,
                                 "room_tag": room_tag,
                                 "player_id": user_id})
        db.session.commit()
    except:
        abort(409)

def insert_current_room(game_id, user_id, room_tag):
    ''' As user plays the game first time, and enters the starting room,
    new entry is created to the current_rooms table
    '''
    sql = "INSERT INTO current_rooms (game_id, room_tag, player_id) VALUES (:game_id, :room_tag, :player_id)"
    try:
        db.session.execute(sql, {"game_id": game_id,
                                 "room_tag": room_tag,
                                 "player_id": user_id})
        db.session.commit()
    except:
        abort(409)

        
def update_current_room(game_id, user_id, room_tag):
    ''' User enters new room, and it is set as the new current_room
    '''
    sql = "UPDATE current_rooms SET room_tag=:room_tag WHERE player_id=:player_id AND game_id=:game_id"
    try:
        db.session.execute(sql, {"game_id": game_id,
                                 "room_tag": room_tag,
                                 "player_id": user_id})
        db.session.commit()
    except:
        abort(409)
    
