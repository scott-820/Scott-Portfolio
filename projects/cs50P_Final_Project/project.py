import sys
import dice, magic8ball

# Some "constants"
NUMDICE = 5
STARTAMOUNT = 100
ANTE = 10
WINAMOUNT = 200
INSTRUCTIONS = """
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
"""

def main():
    # Check for command-line args -h and --help and print INSTRUCTIONS if present
    if len(sys.argv) >= 2:
        if sys.argv[1].lower() == "-h" or sys.argv[1].lower() == "--help":
            print(INSTRUCTIONS)
            sys.exit()
    # Find out if there's a Best Score in "BestScore.txt" and print appropriate message
    score = getBestScore()
    if score == None:
        message = "No one has yet received a Major Award.  See if you can be the first!"
    else:
        message = f"The fewest hands to reach Major Award level so far is {score}. See if you can beat that!"
    print(f"\n{message}")
    input("\nPress Enter to begin. Good luck!")

    # Setup a new game
    playGame = True
    purse = STARTAMOUNT
    d = dice.Dice()                 # make a new set of dice
    for i in range(NUMDICE):        # make the die in the set of dice, all with same value
        die = dice.Die(1)
        d.addDie(die)
    hand = 1                        # first hand at start of new game
    print(f"You have ${purse} to begin with.")
    print(f"\n-- Hand {hand} ----------------------------")

    while playGame:                 # While a game of multiple hands is being played
        # Setup new hand
        playHand = True
        purse -= ANTE               # Reduce purse by ANTE for each new hand
        roll = 1
        d.rollAll()                 # randomize the dice values for the first roll
        print(f"You have ${purse} after your ${ANTE} ante.")
        print(f"Roll Number: {roll}")
        d.drawDice()
        roll = 2                    # set rollcount to 2 since 1st roll has already occurred
        while playHand:             # While an individual hand is being played
            if roll <= 3:
                asking = True
                while asking:       # Ask user for user input
                    inp = input("Enter die numbers to be rolled (Q=Quit, H=Hold): ").upper()
                    if 'Q' in inp:
                        print("-quitting-")
                        playHand = False
                        playGame = False    # Should I just use sys.exit("message")?
                        asking = False      # Can I use while True with breaks?
                    elif 'H' in inp:
                        print("-holding-")
                        roll = 4            # Causes hand to be scored right away
                        asking = False
                    else:
                        # parse numbers and roll selected dice
                        if validDice(inp):
                            dieNumbers = inp.split(" ")
                            for dN in dieNumbers:
                                pos = int(dN) - 1       # To the user, die position is 1-indexed, not 0-indexed
                                #val = random.randint(1,6)
                                #d.replaceDie(pos, val)
                                d.rollADie(pos)
                            print(f"\nRoll Number: {roll}")
                            d.drawDice()
                            roll += 1
                            asking = False
                    if asking:
                        print("Please enter a valid command.")

            else:   # roll >= 3, so score the hand, add winnings to purse and end the hand
                winnings, winStr = calculateScore(d)
                purse += winnings
                print(f"\nYou won ${winnings} with {winStr}.")
                print(f"You have ${purse} remaining.")
                playHand = False
        # end while playHand

        if playGame:    # If user still playing and hasn't quit up above (use sys.exit() above for better logic flow?)
            # Test for game win vs. WINAMOUNT
            if purse >= WINAMOUNT:
                print("\nYou Win!", end="")
                # Test for Best Score here
                h = getBestScore()
                if h == None or h > hand:
                    with open("BestScore.txt", "w") as file:
                        file.write(f"hands={hand}")
                if h > hand:
                    print("... and you made a new Best Score by winning the game with the fewest hands!", end="")
                print("\n")
                print("As your reward, I will tell your fortune.")
                print("Think of a question that has a Yes or No answer.")
                print("Concentrate... and speak your question out loud.")
                input("Hit Enter when ready, and I will divine your future...")
                m8 = magic8ball.Magic8()
                ans = m8.getAnswer()
                print(f'\nThe Magic8 Oracle says: "{ans}"\n')
                #m8.speakAnswer(ans)        # Speak the answer, if not using Codespaces...
                playGame = False            # Game is over

            # Else test if user wants to play another hand
            else:
                while True:
                    userStr = input("Would you like to play another hand? (Y/N) ").strip().upper()
                    if userStr == "N":
                        playGame = False
                        break
                    elif userStr == "Y":
                        # check purse!
                        if purse >= 10:
                            hand += 1
                            print(f"\n-- Hand {hand} ----------------------------")
                        else:
                            print("\nSorry - you have insufficient funds to continue.")
                            print("Please visit our lounge for sympathy and inexpensive refreshments.")
                            playGame = False    # Game is over
                        break

    # end while playGame
    print("\nThanks for playing!")
    print("Program Ended\n")


def validDice(s):
    dice = s.split(" ")
    if len(dice) > 5:
        return False
    for d in dice:
        try:
            num = int(d)
        except ValueError:
            return False
        else:
            if num not in (1,2,3,4,5,6):
                return False
    return True

def getBestScore():
    try:
        file = open("BestScore.txt")
    except FileNotFoundError:
        return None
    else:
        line = file.readline().strip()
        file.close()
        _, n = line.split("=")
        return int(n)

def calculateScore(dce):
    d = []                              # For collecting die values from dice object. Pass this to the check functions.
    if len(dce.diceInSet) == NUMDICE:   # should this be Global?
        for dc in dce.diceInSet:
            d.append(dc.value)
        win = 0
        s = "no qualifying hand"
        if is2Pair(d):              # Scoring is not mutually exclusive so no elif's. Progress "up the ladder"
            win = 5                 # to find the highest scoring match.
            s = "2 Pair"
        if is3ofAKind(d):
            win = 10
            s = "3 of a Kind"
        if isFullHouse(d):
            win = 15
            s = "a Full House"
        if isStraight(d):
            win = 20
            s = "a Straight"
        if is4ofAKind(d):
            win = 25
            s = "4 of a Kind"
        if is5ofAKind(d):
            win = 35
            s = "5 of a Kind"
        return win, s
    else:
        raise ValueError("Incorrect number of dice submitted for scoring")      # Test this with pytest

def is2Pair(d):
    s = set(d)
    if len(s) == 3 and not is3ofAKind(d):
        return True
    else:
        return False

def is3ofAKind(d):
    for i in range(3):
        c = d.count(d[i])
        if c == 3:
            return True
    return False

def is4ofAKind(d):
    for i in range(2):
        c = d.count(d[i])
        if c == 4:
            return True
    return False

def isFullHouse(d):     # Think on this a bit...
    uniqueList = []     # Can't use a set since you can't index into them. Create a list of unique elements instead.
    for val in d:
        if val not in uniqueList:
            uniqueList.append(val)
    if (len(uniqueList) == 2) and (d.count(uniqueList[0]) == 2 or d.count(uniqueList[0]) == 3):
        return True
    else:
        return False

def isStraight(d):
    on = 1 in d
    tw = 2 in d
    th = 3 in d
    fo = 4 in d
    fi = 5 in d
    si = 6 in d
    if (on and tw and th and fo and fi) or (tw and th and fo and fi and si):
        return True
    else:
        return False

def is5ofAKind(d):
    if d.count(d[0]) == 5:
        return True
    else:
        return False


if __name__ == "__main__":
    main()
