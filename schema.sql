CREATE TABLE users (
       id SERIAL PRIMARY KEY,
       locked BOOLEAN DEFAULT false,       
       adm BOOLEAN DEFAULT false,
       username TEXT UNIQUE,
       password TEXT
       );

       
CREATE TABLE messages (
       id SERIAL PRIMARY KEY,
       user_id INTEGER,
       posting_date DATE NOT NULL DEFAULT CURRENT_DATE,
       body TEXT
       );

CREATE TABLE games (
       id SERIAL PRIMARY KEY,
       owner_id INTEGER,
       published BOOL DEFAULT false,
       title TEXT,
       description TEXT,
       start_room TEXT
);

CREATE TABLE rooms (
       game_id INTEGER,
       tag TEXT,
       PRIMARY KEY (tag, game_id),
       title TEXT,
       description TEXT,
       first_visit_description TEXT,
       next_vistis_description TEXT
);
       
CREATE TABLE conditions (
       id SERIAL PRIMARY KEY,
       game_id INTEGER,
       room_tag TEXT,
       all_visited TEXT,
       not_all_visited TEXT,
       all_visited_choice TEXT,
       all_visited_target TEXT
);

CREATE TABLE condition_rooms (
       condition_id INTEGER,
       game_id INTEGER,
       room_tag INTEGER       
);

CREATE TABLE visited_rooms (
       game_id INTEGER,
       room_tag INTEGER,
       player_id INTEGER
);

CREATE TABLE banned_words (
       word TEXT UNIQUE
);   
       
       
