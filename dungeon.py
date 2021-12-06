from db import db


def all_rooms(user_id):
    sql = "SELECT * FROM rooms WHERE owner_id=:user_id ORDER BY tag"
    result = db.session.execute(sql, {"user_id": user_id})
    rooms = result.fetchall()

    sql = "SELECT * FROM conditions WHERE owner_id=:user_id ORDER BY room_tag, id"
    result = db.session.execute(sql, {"user_id": user_id})
    conditions = result.fetchall()

    sql = "SELECT * FROM condition_rooms WHERE owner_id=:user_id ORDER BY room_tag"
    result = db.session.execute(sql, {"user_id": user_id})
    conditions = result.fetchall()    
    
    return {"rooms": rooms,
            "conditions": conditions,
            "condition_rooms": condition_rooms
    }

def create_room(user_id, form):
    sql = '''
    INSERT INTO rooms (
       tag,
       owner_id,
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
       :owner_id,
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
        "owner_id": user_id,
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

    
