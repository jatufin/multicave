CREATE TABLE users (
       id SERIAL PRIMARY KEY,
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

CREATE TABLE dungeons (
       id SERIAL PRIMARY KEY,
       tag TEXT UNIQUE,
       user_id INTEGER,
       description TEXT,
       north_choice TEXT,
       north_target TEXT,
       south_choice TEXT,
       south_target TEXT,
       east_choice TEXT,
       east_target TEXT,
       west_choice TEXT,
       west_target TEXT       
);
       
CREATE TABLE banned_words (
       word TEXT
);   
       
       
