VafiadisCardDiceGame
Description

There is a gambling gathering organized by John Beker, where 14 people attended. Some of the guests like to play dice, some of them like to play cards. John's guests include some who play exclusively dice, some playing only cards but also some playing cards and dice.

Functionality

Each person has a name and each name consists of the first name and the last name. Every dice player has the ability to roll a dice and bring a result.However some players have a technique to roll the dice and manage to bring 6 instead of 5. Some others manage to roll 5 instead of 3. The other players normally roll the dice so they bring from 1-6 with a probability of 1/6 for each possible result.

For the first half of the gathering, all players meet by two each time. If they are both dice players they play a round of dice. If not, they register for the second's half Card game.

Game description

for Dice game: They roll alternately from 10 dice. Every time that the 2 players roll the dice or one brings a bigger result than the other or bring the same result. In the first case, the cumulative is informed score of the player who brought the highest score. In the second case no no score is updated.

for Card game: All available (card) players participate in a hand of cards. In the beginning shuffle the deck and then draw from a card alternately until the cards run out. At the end of the game, each player presents them aces he has and opens his cards. The winner is the one who has collected more aces.

Install dependencies

If you are on a Mac or Linux machine, you probably already have Python installed. In this project we use Python 3.6. We need to make sure though that we install pip and virtualenv for the correct version of Python on your computer. Open a terminal and run the following command:

$ sudo easy_install pip
$ sudo easy_install virtualenv

or if you get an error

sudo -H pip install virtualenv
We clone the repository :

$ git clone https://github.com/PanioVaf/VafiadisCardDiceGame.git
We are creating a virtual enviroment in order to install the dependencies locally.

$ cd VafiadisCardDiceGame/
$ virtualenv .env
$ source .env/bin/activate
$ pip install -r requirements.txt
How to Run

Open the project to IDE (PYCHARM was used for this one) Hit RUN

OR

The commands to run the VafiadisCardDiceGame from terminal is given below.

$ source .env/bin/activate
$ cd src     
$ python card_dice_game.py