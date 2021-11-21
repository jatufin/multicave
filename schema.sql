CREATE TABLE users (
       id SERIAL PRIMARY KEY,
       admin BOOLEAN DEFAULT false,
       public BOOLEAN DEFAULT false,
       username TEXT UNIQUE,
       password TEXT
       );

       
CREATE TABLE messages (
       id SERIAL PRIMARY KEY,
       user_id SERIAL,
       posting_date DATE NOT NULL DEFAULT CURRENT_DATE,
       body TEXT
       );

CREATE TABLE dungeons (
       id SERIAL PRIMARY KEY,
       user_id SERIAL,
       description TEXT,
       north_choice TEXT,
       north_target INTEGER,
       south_choice TEXT,
       south_target INTEGER,
       east_choice TEXT,
       east_target INTEGER,
       west_choice TEXT,
       west_target INTEGER       
);
       

       
       
