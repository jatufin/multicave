CREATE TABLE users (
       id SERIAL PRIMARY KEY,
       locked BOOLEAN DEFAULT false,       
       adm BOOLEAN DEFAULT false,
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
       owner_id INTEGER,
       published BOOL DEFAULT false,
       title VARCHAR(20) NOT NULL,
       description VARCHAR(256),
       start_room VARCHAR(10)
);

CREATE TABLE rooms (
       game_id INTEGER NOT NULL,
       tag VARCHAR(10) NOT NULL,
       PRIMARY KEY (tag, game_id),
       title VARCHAR(30) DEFAULT 'New room',
       description VARCHAR(1000),
       first_visit_description VARCHAR(1000),
       next_visits_description VARCHAR(1000),
       endroom BOOL DEFAULT false
);
       
CREATE TABLE conditions (
       id SERIAL PRIMARY KEY,
       game_id INTEGER NOT NULL,
       room_tag VARCHAR(10) NOT NULL,
       all_visited VARCHAR(200),
       not_all_visited VARCHAR(200),
       all_visited_choice VARCHAR(50),
       all_visited_target VARCHAR(50)
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
       
       
