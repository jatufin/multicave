# Multi Cave - Write and share your own adventure!

## The status of the project
* Fully functionin application can be downloaded from Github
* A demo application is available on heroku server: https://multicave.herokuapp.com/

## Installation

### Donwload and start

Clone the project from GitHub:
```
$ git clone https://github.com/jatufin/multicave
```

The application uses _PostgreSQL_, _Python 3_, _Flask_ and _SQLAlchemy_, which should be installed and environment set up:
* [PostgreSQL](https://www.postgresql.org)
* [Python 3](https://www.python.org/)
* [Flask](https://flask.palletsprojects.com/)
* [SQLAlchemy](https://www.sqlalchemy.org/)

Flask environment can usually be build by running in the project folder:
```
$ python3 -m venv venv
$ . venv/bin/activate
$ pip install Flask
```

And SQL Alchemy libraries:
```
$ pip install flask-sqlalchemy
$ pip install pyscopg2

```

The session management requires, that an evironment variable is set for 16 byte secure key. The variable should contain the key in hexadecimal format:
```
SECURE_KEY
```

### Initializing the database

PostgreSQL database should be up and running. Database tables can be created by running following command in the project directory:

```
$ psql < schema.sql
```

This creates all the tables, buta they are empty. You can sign in a new user with regular privileges, but if you want to give an user admininistrative right in this phase, it has to be done manually directly to the database. For username Rudolf this would be:

```
$ psql
dbname=# UPDATE users SET adm='t' WHERE username='Rudolf';
```

If you rather preoccupy the database with default users and an example game, instead of ```schema.sql``` whole database dump ```pg_database_dump.sql``` should be inserted:

```
$ psql < pg_database_dump.sql
```

Now two default accounts are allreay installed. Adminstrator:

* Administrative account: _admin_
* Password: _admin_

And normal user:
* Normal user account: _Rudolf_
* Passowrd: _pa55word_

You should immeadiately after installation log in as _admin_ and change these passwords.

## Architecture

In the _documentation_ folder there are some helpful diagrams:
* [ER diagram of the database](https://github.com/jatufin/multicave/blob/master/documentation/ER-diagram.svg)
* [Flowcharts](https://github.com/jatufin/multicave/blob/master/documentation/flowcharts.pdf)

For the game structure function, the _Help_ section in the system itself is most recommended. However, the map of the example can be found from the _static_ folder:
* [Flowcharts](https://github.com/jatufin/multicave/blob/master/static/example_game.svg)

The original [Dia](https://wiki.gnome.org/Apps/Dia/) files of these diagrams, are in the _documentation_ directory.

## Description
A web site, where users can create, share and play adventure games. User's can also comment and discuss on a message board.

### Different user accounts
System will have three different types of users: guests, normal users and administrators:

#### Guest
A visitor who opens the main page, can see a list of all the published games, and messages on the messageboard. Guest can't enter any of the games, or send messages to the board.

Operations an guest can do:
* Read messages
* Read game titles, descriptions and publishers
* Sign-up to create a new user account

#### Normal user
A visitor can create a new user providing a user name and password. The username will be used as player's name in the adventures. All normal users can play the games other users have published. Adventures are single user games and all users' game situations are saved in the database, so they can continue playing later from where they left. User can decide, if a game she has created is public or not. The game is visible to other users only, if it has been published. User can advertise, comment games and discuss in a message board.

Message board has a filter, which looks up banned words on subscribed messages. If a message consists banned words, it will not be saved.

Operations an user can do:
* Play games other users have published
* Create a new game and edit it.
* An user can play their own game without publishing it.
* Publish the game they has created, so other users can play it.
* Read and write to the message board.
* Change password


#### Administrator
Administrator is a normal user, who has been granted administrative privileges in addition to normal user right. Administrator can manage user accounts and the banned words list.

Operations an administrator can do:
* Delete an user.
  * All games user is an owner will be deleted.
  * All user's game states will be deleted.
* Prevent user to log in. (freeze an account)
* Change user's password.
* Add administrator rights to an user.
* Remove administrator from an user.
* Delete messages from the message board.
* Add and remove words from the message board filter.

## Games
Games are classical text adventures, where users can move between rooms, and do simple things. The idea is to be more like "choose your own adventure" type book, than to have complex game logic.

To get an idea, here is an example session with a textual user interface
```
******************************************************
* Outside the dungeon                                *

You are on the foothills of a mountain. Sun is
shining and birds are singing. On the rock face to
the North you see dark cave opening.

Do you want to:
  Go North?

You choose to go North!
******************************************************
* Dungeon room                                       *

You are in a big room. You can see corridors going
North, East and West. From the floor you find a key
and put it in your pocket.

Do you want to:
  Go North?
  Go East?
  Go West?

You choose to go West!
******************************************************
* Dungeon room                                       *

You are in a big room. You can see corridors
continuing to North and West. On eastern wall there
is a locked door.

Do you want to:
  Go North?
  Go West?
  Try to open the door with the key?
```

## Message board
Message board is a simple single thread board, which allows only text content.

## Security

To prevent hacking and abuse following guidelines will be followed:
* All form inputs are managed through Flask routes to prevent injections
* Secret session token is used to prevent CSRF attacks
* All route rutines check for login status and prssibly admin right
* All SQL inputs are made through variables, to prevent injections
* All inputs will be filtered to be SQL safe before any processing.
* Server side validation of all inputs.
* All input forms are validated for too big inputs
* All text columns in database user VARCHAR instead of TEXT to limit size
* The message board will have limitations:
  * All messages are filtered for banned words

To perevent cheating in the games:
* No browser side operations will be trust, every input is checked server side.
* Most of the game logic will be implemented inside the database itself.

## Future options
* Guest users could be allowed playing games in some limited way
  * Transferring encrypted game state in HTTP GET requests could be possible
* User could give ratings to the games. (star system)
* Commenting board for each published game.
* Private messages between users.
* Automatic measures might be used to control language used in both message board and in the games.

