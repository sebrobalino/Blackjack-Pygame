Blackjack Game

This is a simple Blackjack game built using Pygame. The game allows the player to place bets, hit or stand, and play against the dealer. It also includes features like peeking at the dealer's card and handling special cases like player and dealer blackjack.

Features

Place bets before each round

Hit or stand to adjust your hand

Peek at the dealer's card when their face-up card is a high value (10, J, Q, K, A)

Handle special cases: player blackjack, dealer blackjack, and player bust

Display player balance and bet amounts

End game screen showing final balance and results

Option to reset the game or leave the table


Installation

Ensure you have Python 3.x installed on your system.

Install Pygame by running the following command:
python3 -m pip install -U pygame --user

Clone or download the project files to your local machine.


Usage

Navigate to the directory containing the project files.

Run the Blackjack game by executing the following command:

python3 blackjack.py

Follow the on-screen instructions to play the game.


Game Instructions


Title Screen:

Enter the starting balance amount and click "Play" to start the game.

Betting Phase:

Place your bets by clicking on the $10, $50, or $100 buttons.
The balance and bet amounts are displayed.
Click "Next" to proceed to the game phase.


Game Phase:

Click "Hit" to draw another card or "Stand" to end your turn.
If the dealer's face-up card is a high value (10, J, Q, K, A), you can click "Peek" to check if the dealer has blackjack.
The balance and bet amounts are displayed.
The player's and dealer's scores can be toggled on or off using the "Show Score?" button.


End of Round:

After the round, the result (win, lose, tie, blackjack) is displayed.
Click "Next" to start a new round or "Leave Table" to go to the end game screen.


End Game Screen:

The final balance is displayed along with a comparison to the starting balance.
Click "Thanks For Playing!" to quit the game.

Contributing
If you'd like to contribute to this project, feel free to fork the repository and submit a pull request.

License
This project is licensed under the MIT License.

Acknowledgements
Pygame Community for their great resources and support.


Enjoy the game and have fun!
