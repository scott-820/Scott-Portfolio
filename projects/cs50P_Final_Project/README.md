# Poker Dice - a CS50P Final Project
### Video Demo: <https://youtu.be/eWxCWPjtxbc>
#### Poker Dice is a python implementation of the classic Poker Dice game. In this variant of the game, the player starts with a $100 purse and attempts to increase that purse to $200 in as few hands as possible, and before they run out of money.

### Useage:

"python project.py -h" or "python project.py --help" will print instructions for the game and then exit<br>
"python project.py" begins a game of poker dice

### Libraries and Packages:
Poker Dice and the custom classes that support it use the sys and random modules that are part of modern Python Standard Libraries.<br>
The Magic8().speakAnswer() class method uses the pyttsx3 package for implementing text to speech, which must be installed with PIP, using:<br>
```pip install pyttsx3```

>__Warning__: This method may not work in cloud-hosted development environments like Codespaces even when the pyttsx3 package is properly installed.

### Gameplay Instructions:
```
Welcome to Poker Dice! Play as many hands as you can before you run out of money.
If you accumulate $200 or more, you win a Major Award!

Every game begins with a $100 purse, and each hand played requires a $10 ante. Take up to 3 rolls
to get the most valuable hand that you can.

Here are the hand values:
    2 Pair:         $5
    3 of a Kind     $10 (return of ante)
    Full House      $15
    Straight        $20
    4 of a Kind     $25
    5 of a Kind     $35

The computer will automatically execute the first roll of each hand.  For rolls 2 and 3,
select the die to be re-rolled by entering the die numbers in a list separated by
spaces. Ex: if you want to re-roll dice 2, 3 and 5 then enter "2 3 5" when prompted.

If you are satisfied with the dice values before your third roll, enter "H" for Hold
and your hand will be immediately scored.
```

### The **"Major Award"**:
When a player accumulates a purse value of $200 or more, they win the game. As a reward, the progam will tell the player's fortune by answering a question that has a Yes or No answer. This behavior is implemented in the Magic8() class.

### Program Structure:
The program is separated into the following major components:
* In the file "project.py":
    * main() function - controls game setup and flow
    * peer level functions to main() - manage hand scoring, file I/O and data validation
* In the file "dice.py":
    * class Die() - represents a single die and it's current value
    * class Dice() - represents a hand of 5 dice and their current values
* In the file "magic8ball.py":
    * class Magic8() - represents a mystical oracle that can answer any Yes/No question

### Design Choices:
Taking an object oriented approach to the design of a single die was intuitive since a die is an obvious, real world object which posesses specific attributes (like face value) and actions that need to be performed (like rolling the die or drawing the die to the console). Extending the concept to modeling a group of 5 dice in a hand seemed equally appropriate, fitting the structure and flow of the game.<br>

However, absent the requirement in this assignment to include multiple functions at the peer level of main() for simplified testing with pytest, the more logical place to include the dice scoring functions (which currently reside in project.py) is inside the dice.Dice() class. Objects of the Dice() class should be able to score themselves, if we were to use OOP more faithfully.  It is as plain as rain though, that these functions remain in main() to satisfy the remit.<br>

The methods and data structures contained in the Magic8() class could have been just as effectively implemented within "project.py" as ordinary functions and variables vs. building them into a class, since the class currently has no specific attributes.  However, it seemed plausible that the class could be extended in the future to include attributes (like multi-language controls, or a setting called "Magic8.notFamilySafe" that enables user-selectable categories of response language); or other methods for relaying the response to users (like Cowsay or some fancy graphics package) such that creating the class up front made sense.


### The main() Function:
The main() function initializes game setup, manages interaction with the user, and implements gameplay logic.<br>
Here is the pseudocode for main():
```
import libraries
import classes

define "constants"

def main():
    if -h or --help cmd-line arg present:
        print instructions
        end program

    setup new game
    while playGame:                         # While playing a game of multiple hands
        setup new hand
        subtract ANTE from purse
        make first dice roll
        while playHand:                     # While playing a hand with multiple rolls
            if roll count <= 3:
                ask user - Quit, Hold or roll specific dice?:
                if Quit:
                    end game
                elif Hold:
                    end hand                # i.e., set roll count = 4
                else roll dice:
                    check for valid roll request
                    roll requested dice
                    increment roll count
            else:                           # i.e., roll count > 3
                score the hand
                add winnings to purse
                end hand
        # end while playHand

        if purse > target WINAMOUNT:
            notify user of win
            if user beat best score:
                notify user of best score
                update "BestScore.txt"
            play Magic8ball                 # i.e., the Major Award
            end game
        else:
            ask user - play another hand?:
                if yes:
                    if purse > ANTE:
                        play next hand
                    if purse < ANTE:
                        notify user
                        end game
                if no:
                    end game
    # end while playgame

# Functions go here

if __name__ == "__main__":
    main()
```
### Other Functions in "project.py"
#### calculateScore(dice: obj Dice()): -> int, str
The calculateScore() function receives a dice.Dice() object, unpacks the dice values for each die in the hand of dice into a list of integers, then passes the list consecutively to each of the score evaluation functions discussed further below to determine the highest dollar value match.<br>
It will return a tuple that includes the highest $ value score as an integer, and a description of the match type as a string.  For example, if the submitted Dice() object contains 3 dice with the same value, the function will return the tuple (10, "3 of a Kind").
```
    :param dice: a dice.Dice() object to be scored
    :type dice: dice.Dice() object
    :return: a tuple holding score and match type
    :rtype: tuple(int, string)
```

#### is2Pair(d: list(int)) -> bool:
This function accepts a list of 5 integers as an input, and returns "True" if the submitted Dice() object contains 2 pair. Otherwise it returns "False".
```
    :param d: a list of dice values as integers to be evaluated
    :type d: integer list()
    :return: True if list contains two pair, otherwise False
    :rtype: bool
```

#### is3ofAKind(d: list(int)) -> bool:
This function accepts a list of 5 integers as an input, and returns "True" if the submitted Dice() object contains 3 and only 3 dice of the same value. Otherwise it returns "False".
```
    :param d: a list of dice values as integers to be evaluated
    :type d: integer list()
    :return: True if list contains 3 of a kind, otherwise False
    :rtype: bool
```

#### isFullHouse(d: list(int)) -> bool:
This function accepts a list of 5 integers as an input, and returns "True" if the submitted Dice() object contains 3 dice with the same value and two dice that have the same value (but a different value from the other 3 dice). Otherwise it returns "False".
```
    :param d: a list of dice values as integers to be evaluated
    :type d: integer list()
    :return: True if list contains 3 of a kind and a pair, otherwise False
    :rtype: bool
```

#### is2Straight(d: list(int)) -> bool:
This function accepts a list of 5 integers as an input, and returns "True" if the submitted Dice() object contains dice with 5 consecutive values - 1 through 5 or 2 through 6. Otherwise it returns "False".
```
    :param d: a list of dice values as integers to be evaluated
    :type d: integer list()
    :return: True if list contains 5 integers in sequence, otherwise False
    :rtype: bool
```

#### is4ofAKind(d: list(int)) -> bool:
This function accepts a list of 5 integers as an input, and returns "True" if the submitted Dice() object contains 4 and only 4 dice of the same value. Otherwise it returns "False".
```
    :param d: a list of dice values as integers to be evaluated
    :type d: integer list()
    :return: True if list contains 4 of a kind, otherwise False
    :rtype: bool
```

#### is5ofAKind(d: list(int)) -> bool:
This function accepts a list of 5 integers as an input, and returns "True" if the submitted Dice() object contains 5 dice of the same value. Otherwise it returns "False".
```
    :param d: a list of dice values as integers to be evaluated
    :type d: integer list()
    :return: True if list contains 5 of a kind, otherwise False
    :rtype: bool
```

#### isvalidDice(s: str) -> bool:
This function accepts an input parameter of type str and returns "True" if the string can be successfully separated into a list of integers when split on spaces (" "), and if those integers are within the set of numbers 1 through 6. Otherwise the function returns "False".<br>

If any of the split elements cannot be converted to interger, the function will raise a ValueError.
```
    :param s: a string to be parsed and evaluated
    :type s: str
    :raise ValueError: If string parsed on spaces has elements which are not convertable to integer type
    :return: True if parsed elements are integer type and in the set (1,2,3,4,5,6) and False otherwise
    :rtype: bool
```

### The Die() Object: (see filename: "dice.py")
This object represents a single die with a face value that is implemented as a property. Other attributes include a list of strings called self.rows which holds five string values that represent the 5 rows to be printed when drawing the die in the termanal with a "dot pattern" reflective of the \_value property.<br>

Class variables are used to hold the unicode character values for drawing the ASCII box art symbols to the terminal. The box art symbols are used to create the image of a die with the correct number of dots corresponding to the _value property.<br>

The unicode characters for ASCII box drawing can be found here: <https://en.wikipedia.org/wiki/Box-drawing_characters>

A data construct was required to make row/string generation for a die's printed image easier to program. The construct chosen for this design is a dictionary called DOTS{}, shown in the code snippet below.  DOTS{} has integer dictionary _keys_ that correspond to the 6 possible values of the \_value property. The _keys_ are paired with dictionary _values_ that are lists of three 3-tuples.  Each list of three 3-tuples has 9 symbols that represent a 3 x 3 matrix used for drawing the die's dots.  The symbols are one of two values: _space_ or _black circle_.  Using these two symbols, the traditional dot patterns for die values 1 to 6 can be programmatically created (see the genRows() method below).
```python
    # Class variables for unicode ASCII box art characters.
    TOP = '\u256D'+'\u2500'+'\u2500'+'\u2500'+'\u2500'+'\u2500'+'\u2500'+'\u2500'+'\u256E'
    BOTTOM = '\u2570'+'\u2500'+'\u2500'+'\u2500'+'\u2500'+'\u2500'+'\u2500'+'\u2500'+'\u256F'
    VERT = '\u2502' # vertical line character
    SP = ' '
    BC = '\u25CF'   # this is the Black Circle character
    DOTS = {
        1:[(SP,SP,SP),(SP,BC,SP),(SP,SP,SP)],
        2:[(BC,SP,SP),(SP,SP,SP),(SP,SP,BC)],
        3:[(BC,SP,SP),(SP,BC,SP),(SP,SP,BC)],
        4:[(BC,SP,BC),(SP,SP,SP),(BC,SP,BC)],
        5:[(BC,SP,BC),(SP,BC,SP),(BC,SP,BC)],
        6:[(BC,SP,BC),(BC,SP,BC),(BC,SP,BC)],
    }
```

__Methods include:__
#### __init__(self, v):
Initializes the _value property with the integer input parameter v and creates the 5 strings in the self.rows[] list based on self._value used for printing the die.
```python
    def __init__(self, value):
        self._value = value         # This is a property and can't be modified directly by the user
        self.rows = []              # this holds a list of strings for drawing the die
        self.genRows()              # Calls method to create the rows
```

#### setDieValue(self, v):
Sets the _value property to v and updates the strings in the self.rows list to reflect the new value.
```python
    def setDieValue(self, v):
        self._value = v             # _valule is a property
        self.genRows()
```

#### rollDie(self):
Sets the _value property to a random number between 1 and 6, inclusive and updates the strings in the self.rows list to reflect the new value.
```python
    def rollDie(self):
        from random import randint
        self.setDieValue(randint(1,6))
```

#### genRows(self):
Generates the 5 strings for drawing the die and places them in the self.rows[] list
```python
    def genRows(self):                  # Creates the rows based on _value indexing into DOTS
        self.rows = []
        self.rows.append(Die.TOP)       # Add the top row characters
        for j in range(3):              # dots and spaces are in a 3x3 structure
            r = Die.VERT + Die.SP       # Start the left side of a middle row
            for i in range(3):
                r = r + Die.DOTS[self._value][j][i]
                r = r + Die.SP
            r = r + Die.VERT
            self.rows.append(r)
        self.rows.append(Die.BOTTOM)    # Add the bottom row characters
```

#### draw(self):
Draws the die to the terminal by printing the 5 strings in self.rows[].
```python
    def draw(self):                 # Draws the die, row by row
        for row in self.rows:
            print(row)
```

### The Dice() Object: (see filename: "dice.py")
This object represents a "hand" of 5 dice (i.e. 5 Die() objects), used in the Poker Dice game. When initialized, the object contains no Die objects - they must be added to the Dice() object via the addDie() method (see below).<br>

The only attribute in a Dice() object is a list named self.diceInSet[] which holds Die() objects. self.diceInSet[] is initialized to an empty list in the __init__() method.

__Methods include:__
#### __init__(self):
Initializes the attribute self.diceInSet[] to an empty list.
```python
    def __init__(self):
        self.diceInSet = []         # Holds the die objects in a "hand". Add die using AddDie().
```

#### addDie(self, d):
Accepts an object of class Die() as an input parameter and adds the Die() object to the list self.diceInSet[].  If the user attempts to add more than 7 die to the Dice() object, the add will be rejected and a ValueError will be raised.
```python
    def addDie(self, d):
        # d is an object of class Die
        if len(self.diceInSet) >= 8:
            raise ValueError("Limit of 7 die in hand of dice.")
        else:
            self.diceInSet.append(d)
```

#### rollAll(self):
Rolls all Die() objects in Dice(), updating Die() values (and corresponding strings in rows[]) with random numbers between 1 and 6 inclusive.
```python
    def rollAll(self):
        for i in range(len(self.diceInSet)):
            self.diceInSet[i].rollDie()
```

#### rollADie(self, pos):
Rolls the Die() object at position self.diceInSet[pos], updating Die() value (and corresponding strings in rows[]) with a random number between 1 and 6 inclusive.  Note that pos is integer, and is 0-indexed to correspond to the Die() objects in self.diceInSet.
```python
    def rollADie(self, pos):
        if pos > len(self.diceInSet):
            raise ValueError("Position out of range")
        else:
            self.diceInSet[pos].rollDie()
```

#### replaceDie(self, pos, v):
Updates the Die() object at position self.diceInSet[pos], setting Die() value (and corresponding strings in rows[]) to the integer value v.  Note that pos is integer, and is 0-indexed to correspond to the Die() objects in self.diceInSet.
```python
    def replaceDie(self, pos, v):
        if pos > len(self.diceInSet):
            raise ValueError("Position out of range")
        elif v not in (1,2,3,4,5,6):
            raise ValueError("Value out of range")
        else:
            self.diceInSet[pos].setDieValue(v)
```

#### drawDice(self):
Draws all Die() objects in the Dice() object to the console side by side with spaces between each of the Die() images. Each Die() in Dice() has 5 rows of strings that represent the die's image. The first row of each die must be concactenated into one Big First Row for printing the dice side by side. Likewise, Big Second, Third, Fourth and Fifth Rows need to be created and printed as well.  The method adds a 6th Big Row that prints the Die numbers in the hand as labels, centered below each die image. See code snippet below:
```python
    def drawDice(self):
        bigRows = []                                    # Holds the per-line info for each die in the dice object
        for i in range(len(self.diceInSet)):
            bigRow = ""
            for d in self.diceInSet:                    # for each die in the list of dice...
                bigRow += d.rows[i] + " "
            bigRows.append(bigRow)
        bigRow = ""
        for i in range(len(self.diceInSet)):            # Draw last line with die numbers, centered per die
            bigRow += "    " + str(i+1) + "     "
        bigRows.append(bigRow)
        for bigRow in bigRows:                          # Print out the concactenated rows
            print(bigRow)
```

### The Magic8() Object: (see filename: "magic8ball.py")
This object represents a magical oracle that can see past, present and future. It provides an answer to any question that has a "Yes" or "No" answer by selecting that answer at random from a built-in list of potential answers.<br>

This class currently has no initialization values or attributes. It does include as a class variable - a list of potential answers to Yes/No questions, called ANSWERS[] (see snippet below)
```python
    ANSWERS = [
        "It is decidedly so.",
        "Don't count on it.",
        "It is certain.",
        "My reply is no.",
        "My sources say no.",
        "Yes, definitely.",
        "Outlook not so good.",
        "You may rely on it.",
        "Very doubtful.",
        "As I see it, yes.",
        "Signs point to yes.",
        "I should hope not.",
        "Most likely.",
        "No - and don't take any wooden Bitcoin.",
        "Outlook is promising.",
    ]
```
__Methods include:__
#### __init__(self):
No functionality at present.
```python
    def __init__(self):
        pass
```

#### getAnswer(self):
Takes no input parameters and returns a random item from the list Magic8.ANSWERS, as a string.
```python
    def getAnswer(self):
        from random import randint
        n = randint(0,len(Magic8.ANSWERS)-1)
        return Magic8.ANSWERS[n]
```

#### speakAnswer(self, answer):
Takes a string answer as an input, passes that string to an instance of the the pyttsx3 engine class, and causes the engine to speak "The Magic 8 Oracle says:", followed by speaking the text string defined by the input parameter 'answer'.  The method returns no parameters.  See code snippet below.

>__Warning__: Use of this method requires that the pyttsx3 package be installed using PIP (pip install pyttsx3). It may not work in cloud-hosted development environments like Codespaces even when the package is properly installed.
```python
    def speakAnswer(self, answer):      # Don't use this method if executing in Codespaces
        import pyttsx3                  # Works fine in stand-alone VS Code on Windows
        engine = pyttsx3.init()
        engine.say(f"The Magic 8 Oracle says:")
        engine.runAndWait()             # Generates a pause between speaking the two strings
        engine.say(answer)
        engine.runAndWait()
```

#### End of README.md
