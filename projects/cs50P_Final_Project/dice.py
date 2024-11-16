class Die:
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

    def __init__(self, value):
        self._value = value         # don't want this to be modifiable directly by the user
        self.rows = []              # this holds a list of strings for drawing the die
        self.genRows()              # Calls method to create the rows

    @property
    def value(self):
        return self._value

    def setDieValue(self, v):       # Value should not be directly accessible
        self._value = v
        self.genRows()

    def rollDie(self):
        from random import randint
        self.setDieValue(randint(1,6))

    def genRows(self):              # Creates the rows based on _value indexing into DOTS
        self.rows = []
        self.rows.append(Die.TOP)   # Add the top row characters
        for j in range(3):          # dots and spaces are in a 3x3 structure
            r = Die.VERT + Die.SP   # Start the left side of a middle row
            for i in range(3):
                r = r + Die.DOTS[self._value][j][i]
                r = r + Die.SP
            r = r + Die.VERT
            self.rows.append(r)
        self.rows.append(Die.BOTTOM) # Add the bottom row characters

    def draw(self):                 # Draws the die, row by row
        for row in self.rows:
            print(row)

class Dice:
    def __init__(self):
        self.diceInSet = []         # Holds the die objects in a "hand". Add die using AddDie().

    def addDie(self, d):
        # d is an object of class Die
        if len(self.diceInSet) >= 8:
            raise ValueError("Limit of 7 die in hand of dice.")
        else:
            self.diceInSet.append(d)

    def rollAll(self):
        #from random import randint
        for i in range(len(self.diceInSet)):
            #self.diceInSet[i].setDieValue(randint(1,6))
            self.diceInSet[i].rollDie()

    def rollADie(self, pos):
        if pos > len(self.diceInSet):
            raise ValueError("Position out of range")
        else:
            self.diceInSet[pos].rollDie()

    def replaceDie(self, pos, v):
        if pos > len(self.diceInSet):
            raise ValueError("Position out of range")
        elif v not in (1,2,3,4,5,6):
            raise ValueError("Value out of range")
        else:
            self.diceInSet[pos].setDieValue(v)          # this will call die.getRows(), too

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


def main():
    from random import randint

    while True:
        inp = input("Enter die value (1-6) or Q to Quit: ").strip().upper()
        if inp == "Q":
            break
        try:
            i = int(inp)
        except ValueError:
            pass
        else:
            d = Die(i)
            d.draw()

    print("\nMake a hand of dice and print them.")
    dice = Dice()
    for _ in range(1, 6):
        i = randint(1,6)
        d = Die(i)
        dice.addDie(d)
    dice.drawDice()

    input("\nHit Enter to re-roll all dice.")
    dice.rollAll()
    dice.drawDice()

    input("\nHit Enter to re-roll dice 1, 3 and 5")
    dice.rollADie(0)
    dice.rollADie(2)
    dice.rollADie(4)
    dice.drawDice()

    input("\nHit Enter to set dice 2 and 4 to the value 5.")
    val = 5
    dice.replaceDie(1, val)
    dice.replaceDie(3, val)
    dice.drawDice()

    print("\nEnd Program")

if __name__ == "__main__":
    main()
