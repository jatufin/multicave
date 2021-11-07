# Multi Cave
A web site, where users can create and share adventure games. Users can play and comment another user's games.

## Different users

### Normal user
Site visitor can create a new user providing a user name and password. The username will be used as player's name in the adventures user plays.

Users can change the password.

All normal users can play other users' published games. Adventures are single user games, but all users game situations are saved in the database, so they can continue playing later from where they left.

All users can create a new game, and edit it.

User can decide, if a game she has created is published or not. The game is visible to other users only, if it has been published.

The site has a simple message board, where users can write comments and advertise their newest creation.

### Administrator

Administrator can create and delete users, and set their password. An user account can also be freezed, when it's not allowed to log in, but games are still available to other users.

Administrators can edit and delete all games, both published and unpublished.

## Games
Games are text based, where users can move between rooms, and do simple things.

To get an idea, here is an example session with text user interface
```
* Outside the dungeon *

You are on the foothills of a mountain. On the rock face to the North you see cave opening.

You can:
go north

What do you want to do? GO NORTH

* Dungeon room *

You are in a big room. You can see corridors goin North, East and West.
On the floor is a key.

You can:
go North, East or West
take the key

What do you want to do? TAKE THE KEY
You took the key.

* Dungeon room *

You are in a big room. You can see corridors goin North, East and West.

You can:
go North, East or West
What do you want to do?
```

## Message board
Message board is a simple single thread board, which allows only text content.

## Security
Control measures will be made to prevent abuse:
* Single user can create and publish only limited number of games in time.
* Single user can publish only limited number of messages in time.
* Message length is limited.
* Automatic measures might be used to control language used in both message board and in the games. This should be included at least as an easily implementable option to the system.

## Future options
* User could give ratings to the games (star system)
* Commenting board for each published game
* Private messages between users
