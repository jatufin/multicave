# Multi Cave - Write and share your own adventure!

## The status of the project
Currently only basic funktionality has been implemented:
* Loginin and logout
* Visitor can sign up and create a new account
* A message board is shown on front page
* Logged in user can send messages to the board
* Dungeon edit page is available, and user can create new rooms to their dungeon
* No game play has yet been implemented
* Appearance has not been fine tuned in any way

A web site, where users can create, share and play adventure games. User's can also comment and discuss on a message board.

## Different user accounts
System will have three different types of users: guests, normal users and administrators:

### Guest
Guest user is anyone, who opens the web page, but is not signed in.

A guest can:
* See a description about the service.
* See the message board.
* Create an user account to become normal user.

### Normal user
A visitor can create a new user providing a user name and password. The username will be used as player's name in the adventures user plays. All normal users can play other users' published games. Adventures are single user games, but all users game situations are saved in the database, so they can continue playing later from where they left. User can decide, if a game she has created is public or not. The game is visible to other users only, if it has been published. User can advertise, comment games and discuss in a message board.

Operations an user can do:
* Change password.
* Play games other users have published
* Create a new game, and edit it.
* Publish the game she has created.
* Read message board.
* Write messages to the message board.


### Administrator
Administrator is a normal user, who has been granted administrative privileges in addition to normal user right. Administrator can manage user accounts and all the games in the database.

Operations an administrator can do:
* Delete an user.
  * All games user is an owner will be deleted.
  * All user's game states will be deleted.
* Prevent user to log in. (freeze an account)
* Change user's password.
* Add administrator rights to an user.
* Remove administrator from an user.
* Delete any game, published or not.
* Edit all games.
* Change the owner of a game.
* Delete messages from the message board.

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
* All inputs will be filtered to be SQL safe before any processing.
* Server side validation of all inputs.
* Size limits to prevent denial of service attacks:
  * Games can have only maximum number of rooms.
  * Limits to text sizes and variable numbers in games.
* Single user can create and publish only limited number of games in time.
* The message board will have limitations:
  * Single user can publish only limited number of messages in time.
  * Message length is limited.

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

