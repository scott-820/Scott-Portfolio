# Scotzee
## A Familiar Dice Game with an Exceedingly Clever Name
Scotzee is a dice game where the player tries to maximize their score in a game of 13 rounds across 13 different scoring categories.
#### Watch a video demo of the project here: <https://youtu.be/xRx9d-cMRj8>
## Game Play
>For each of the 13 rounds in a game, players will roll 5 dice up to three times, trying to find the best score not yet used in the game. On the first roll, all 5 dice are rolled. For subsequent rolls in a round, players may choose to re-roll all of the dice or, any subset of the die \(withholding the remainder from that roll). A player need not roll 3 times in a round if they wish to score their dice after the first or second roll.<br>

>Every round must conclude with the selection of a scoring category and each of scoring categories may be selected only once in a game. At times, a player may need to select a scoring category that is not satisfied by the dice values, wherein a score of 0 will be applied to the category. When pressed to do so, players will frequently "zero out" the Scotzee category first since it is the hardest category to satisy.

>The scoring categories are broken into the upper half and the lower half.
### The upper half categories:
* Ones
* Twos
* Threes
* Fours
* Fives
* Sixes
>Scoring in these categories is calculated by taking the category value (one through six) times the number of dice in the hand with that value. For example, if at the end of the round a player has three 4's, a 5 and a 2, then the score for the "Fours" category would be 4 x 3 = 12. The 5 and the 2 are not be counted in the score.

>A bonus of 35 points is awarded to the player if the total of the upper category scores (Ones through Sixes) is 63 or greater.

### The lower half categories:
* 3 of a Kind:  Must have at least 3 dice of the same value. Scoring is the total of all 5 dice.
* 4 of a Kind:  Must have at least 4 dice of the same value. Scoring is the total of all 5 dice.
* Full House:   Must have 3 dice of one value and 2 dice of another value. Score is always 25.
* Small Straight:  Must have 4 dice in sequence (1-4, 2-5 or 2-6). Score is always 30.
* Large Straight:  Must have 5 dice in sequence(1-5 or 2-6). Score is always 40.
* Scotzee:  Must have 5 dice of the same value. Score is always 50 when the Scotzee scoring category is selected.
>Additional Scotzees can be applied to any other lower half scoring category and will automatically satisy that category.  For example, if a second Scotzee of 5's is rolled \(the Scotzee category has been previously chosen) and the player selects the Full House scoring category, then Full House will be scored at 25 points.

>Additional Scotzees can also satisfy upper half scoring categories, but only to the category that matches the value of the dice. For example if a second Scotzee of 5's is rolled \(the Scotzee category has been previously chosen), then the player could apply the roll to the "Fives" category, where it would score 25 points, i.e. the sum of all five 5's.

>Each additional Scotzee will also add a 100 point lower half bonus to the overall game score.

## The Scotzee Program:
As with most of the games I've written in Python, Scotzee.py is based on the Pygame package \(pip install pygame), the documentation for which can be found here: <https://www.pygame.org/docs/>
>**Note:** The fonts used in the progam are part of the standard Windows font package. If you are using a Linux or Mac OS, then you will likely have to install Windows fonts on your system, or modify the code to use equivalent or alternative fonts.
### Program Files:
#### scotzee.py:
Game flow and logic is managed in this file, primarily within the main() function, which implments a fairly standard pygame loop which repeatedly:
* Draws game elements to the screen
* Checks mouse-enabled elements for mouse clicks/selection, responding appropriately
* Checks for events (just pygame.QUIT in this program), responding appropriately

The pygame loop normally will handle movement of elements on the screen as well, however Scotzee has no moving elements to handle.
>**Note:** The graphics files used in scotzee.py are all located in the folder "./graphics"
#### settings.py:
This file contains the game settings and "constants". Use "from settings import *" to avoid prefixing "settings." to items referenced in settings.py.
