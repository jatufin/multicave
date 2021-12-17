CREATE TABLE users (
       id SERIAL PRIMARY KEY,
       locked BOOLEAN DEFAULT false NOT NULL,       
       adm BOOLEAN DEFAULT false NOT NULL,
       username VARCHAR(12) UNIQUE NOT NULL,
       password VARCHAR(128) NOT NULL
       );

       
CREATE TABLE messages (
       id SERIAL PRIMARY KEY,
       user_id INTEGER NOT NULL,
       posting_date DATE NOT NULL DEFAULT CURRENT_DATE,
       body VARCHAR(1024) NOT NULL
       );

CREATE TABLE games (
       id SERIAL PRIMARY KEY,
       owner_id INTEGER NOT NULL,
       published BOOL DEFAULT false NOT NULL,
       title VARCHAR(40) DEFAULT 'New game' NOT NULL,
       description VARCHAR(256) DEFAULT '',
       start_room VARCHAR(10) DEFAULT ''
);

CREATE TABLE rooms (
       game_id INTEGER NOT NULL,
       tag VARCHAR(10) NOT NULL,
       PRIMARY KEY (tag, game_id),
       title VARCHAR(30) DEFAULT 'New room' NOT NULL,
       description VARCHAR(1000) DEFAULT '',
       first_visit_description VARCHAR(1000) DEFAULT '',
       next_visits_description VARCHAR(1000) DEFAULT '',
       endroom BOOL DEFAULT false NOT NULL
);
       
CREATE TABLE conditions (
       id SERIAL PRIMARY KEY,
       game_id INTEGER NOT NULL,
       room_tag VARCHAR(10) NOT NULL,
       all_visited VARCHAR(200) DEFAULT '',
       not_all_visited VARCHAR(200) DEFAULT '',
       all_visited_choice VARCHAR(50) DEFAULT '',
       all_visited_target VARCHAR(10) DEFAULT ''
);

CREATE TABLE condition_rooms (
       condition_id INTEGER NOT NULL,
       game_id INTEGER NOT NULL,
       room_tag VARCHAR(10) NOT NULL       
);

CREATE TABLE visited_rooms (
       game_id INTEGER NOT NULL,
       room_tag VARCHAR(10) NOT NULL,
       player_id INTEGER NOT NULL
);

CREATE TABLE current_rooms (
       game_id INTEGER NOT NULL,
       room_tag VARCHAR(10) NOT NULL,
       player_id INTEGER NOT NULL
);

CREATE TABLE banned_words (
       word VARCHAR(30) UNIQUE NOT NULL
);   
       
       
