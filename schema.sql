CREATE TABLE users (
       id SERIAL PRIMARY KEY,
       locked BOOLEAN DEFAULT false,       
       admin BOOLEAN DEFAULT false,
       public BOOLEAN DEFAULT false,
       username TEXT UNIQUE,
       password TEXT
       );

       
CREATE TABLE messages (
       id SERIAL PRIMARY KEY,
       user_id INTEGER,
       posting_date DATE NOT NULL DEFAULT CURRENT_DATE,
       body TEXT
       );

CREATE TABLE rooms (
       tag TEXT,
       owner_id INTEGER,
       PRIMARY KEY (tag, owner_id),
       description TEXT,
       first_visit_description TEXT,
);

CREATE TABLE visited_rooms (
       room_tag INTEGER,
       owner_id INTEGER,
       player_id INTEGER
);
       
CREATE TABLE conditions (
       id SERIAL PRIMARY KEY,
       owner_id INTEGER,
       room_tag TEXT,
       all_visited TEXT,
       not_all_visited TEXT,
       all_visited_choice TEXT,
       all_visited_target TEXT
);

CREATE TABLE condition_rooms (
       owner_id INTEGER,
       condition_id INTEGER,
       room_tag INTEGER       
);

CREATE TABLE banned_words (
       word TEXT UNIQUE
);   
       
       
