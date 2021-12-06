from flask import session, abort
from db import db

def get_public_games(): # TODI: Check if the user is marked it as public
    sql = "SELECT * FROM games WHERE published='t'"
    result = db.session.execute(sql)
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

def get_game(game):
    game_id = game.id
    rooms = get_all_rooms(game_id)
    conditions = get_conditions(game_id)
    condition_rooms = get_condition_rooms(game_id)

    return {"main": game,
            "rooms": rooms,
            "conditions": conditions,
            "condition_rooms": condition_rooms}


def get_room(game_id, tag):
    sql = "SELECT * FROM rooms WHERE game_id=:game_id AND tag=:tag"
    result = db.session.execute(sql, {"game_id": game_id, "tag": tag})
    rooms = result.fetchall()

    if not rooms:
        return None

    return rooms[0]


def get_all_rooms(game_id):
    sql = "SELECT * FROM rooms WHERE game_id=:game_id ORDER BY tag"
    result = db.session.execute(sql, {"game_id": game_id})
    rooms = result.fetchall()

    return rooms


def new_room(form):
    user_id = session["user_id"]
    game_id = form["game_id"]
    tag = form["tag"]

    if not is_owner(game_id, user_id):
        abort(401)

    if not tag:
        return
    
    if get_room(game_id, tag):  # Room already exists
        return

    sql = "INSERT INTO rooms (game_id, tag) VALUES (:game_id, :tag)"
    try:
        db.session.execute(sql, {"game_id": game_id, "tag": tag})
        db.session.commit()
    except:
        abort(401)
        
        
def update_room(form):
    user_id = session["user_id"]
    game_id = form["game_id"]

    if not is_owner(game_id, user_id):
        abort(401)

    tag = form["tag"]
    title = form["title"]
    description = form["description"]
    first_visit_description = form["first_visit_description"]
    next_visits_description = form["next_visits_description"]
    
    endroom = "True" if form.get("endroom_selection") else "False"

    
    # sql = "UPDATE rooms SET title=:title, description=:description, first_visit_description=:first_visit_description, next_visits_description=:next_visits_description, endroom=:endroom WHERE game_id=:game_id AND tag=:tag"

    sql = "UPDATE rooms SET title=:title, description=:description, first_visit_description=:first_visit_description, next_visits_description=:next_visits_description, endroom=:endroom WHERE game_id=:game_id AND tag=:tag"

    try:
        db.session.execute(sql, {"game_id": game_id,
                                 "tag": tag,
                                 "title": title,
                                 "description": description,
                                 "first_visit_description": first_visit_description,
                                 "next_visits_description": next_visits_description,
                                 "endroom": endroom})
        db.session.commit()
    except:
        abort(409)    
        
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


def new_condition(form):
    user_id = session["user_id"]
    game_id = form["game_id"]

    if not is_owner(game_id, user_id):
        abort(401)

    room_tag = form["room_tag"]

    sql = "INSERT INTO conditions (game_id, room_tag) VALUES (:game_id, :room_tag)"
    try:
        db.session.execute(sql, {"game_id": game_id, "room_tag": room_tag})
        db.session.commit()
    except:
        abort(401)

        
def update_condition(form):
    user_id = session["user_id"]
    game_id = form["game_id"]

    if not is_owner(game_id, user_id):
        abort(401)

    id = form["id"]
    all_visited = form["all_visited"]
    not_all_visited = form["not_all_visited"]
    all_visited_choice = form["all_visited_choice"]
    all_visited_target = form["all_visited_target"]

    sql = "UPDATE conditions SET all_visited=:all_visited, not_all_visited=:not_all_visited, all_visited_choice=:all_visited_choice, all_visited_target=:all_visited_target WHERE id=:id"
    try:
        db.session.execute(sql, {"id": id,
                                 "all_visited": all_visited,
                                 "not_all_visited": not_all_visited,
                                 "all_visited_choice": all_visited_choice,
                                 "all_visited_target": all_visited_target})
        db.session.commit()
    except:
        abort(401)

    

       
def delete_condition(form):
    user_id = session["user_id"]
    game_id = form["game_id"]

    if not is_owner(game_id, user_id):
        abort(401)

    id = form["id"]
    sql_cond = "DELETE FROM conditions WHERE id=:id"
    sql_rooms = "DELETE FROM condition_rooms WHERE condition_id=:id"
    
    try:
        db.session.execute(sql_cond, {"id": id})
        db.session.execute(sql_rooms, {"id": id})
        db.session.commit()
    except:
        abort(401)
    

def new_conditionroom(form):
    user_id = session["user_id"]
    game_id = form["game_id"]

    if not is_owner(game_id, user_id):
        abort(401)

    condition_id = form["condition_id"]
    room_tag = form["room_tag"]

    if not room_tag:
        return
    
    sql = "INSERT INTO condition_rooms (condition_id, game_id, room_tag) VALUES (:condition_id, :game_id, :room_tag)"

    try:
        db.session.execute(sql, {"condition_id": condition_id,
                                 "game_id": game_id,
                                 "room_tag": room_tag})
        db.session.commit()
    except:
        abort(401)
    
def remove_conditionroom(form):
    user_id = session["user_id"]
    game_id = form["game_id"]

    if not is_owner(game_id, user_id):
        abort(401)

    condition_id = form["condition_id"]
    room_tag = form["room_tag"]

    sql = "DELETE FROM condition_rooms WHERE condition_id=:condition_id AND game_id=:game_id AND room_tag=:room_tag"
    try:
        db.session.execute(sql, {"condition_id": condition_id,
                                 "game_id": game_id,
                                 "room_tag": room_tag})
        db.session.commit()
    except:
        abort(401)
    
    
def create_game(user_id):
    sql = "INSERT INTO games (owner_id) VALUES (:owner_id)"
    try:
        db.session.execute(sql, {"owner_id": user_id})
        db.session.commit()
    except:
        abort(401)

        
def update_game(form):
    user_id = session["user_id"]
    game_id = form["game_id"]

    if not is_owner(game_id, user_id):
        abort(401)
        
    title = form["title"]
    description = form["description"]
    published = "True" if form.get("published_selection") else "False"
    start_room = form["start_room"]
    
    sql = "UPDATE games SET title=:title, description=:description, published=:published, start_room=:start_room WHERE id=:game_id"

    try:
        db.session.execute(sql, {"game_id": game_id,
                                 "title": title,
                                 "description": description,
                                 "published": published,
                                 "start_room": start_room})
        db.session.commit()
    except:
        abort(409)    
        
def is_owner(game_id, user_id):
    sql = "SELECT * FROM games WHERE id=:game_id AND owner_id=:user_id"
    result = db.session.execute(sql, {"game_id": game_id, "user_id": user_id})
    games = result.fetchall()

    return True if games else False
                                      
