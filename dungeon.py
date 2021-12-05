from flask import session, abort
from db import db

def all_rooms(user_id):
    sql = "SELECT * FROM dungeons WHERE user_id=:user_id"
    result = db.session.execute(sql, {"user_id":user_id})
    rooms = result.fetchall()

    return rooms

def create_room(user_id, form):
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
        "tag": form["tag"],
        "user_id": user_id,
        "description": form["description"],
        "north_choice": form["north_choice"],
        "north_target": form["north_target"],
        "south_choice": form["south_choice"],
        "south_target": form["south_target"],
        "east_choice": form["east_choice"],
        "east_target": form["east_target"],
        "west_choice": form["west_choice"],
        "west_target": form["west_target"]
    }
    db.session.execute(sql, values)
    db.session.commit()

    
