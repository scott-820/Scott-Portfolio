import pygame
from random import choice
import button, dice, checkBox
from settings import *

# Initilize game setup and Start Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))            # Create a Pygame surface called "screen"
pygame.display.set_caption('Scotzee!')

new_img = pygame.image.load("./graphics/New.png").convert_alpha()
quit_img = pygame.image.load("./graphics/Quit.png").convert_alpha()
continue_img = pygame.image.load("./graphics/Continue.png").convert_alpha()
d0_img = pygame.image.load("./graphics/Zero.png").convert_alpha()
d1_img = pygame.image.load("./graphics/One.png").convert_alpha()
d2_img = pygame.image.load("./graphics/Two.png").convert_alpha()
d3_img = pygame.image.load("./graphics/Three.png").convert_alpha()
d4_img = pygame.image.load("./graphics/Four.png").convert_alpha()
d5_img = pygame.image.load("./graphics/Five.png").convert_alpha()
d6_img = pygame.image.load("./graphics/Six.png").convert_alpha()
dieImages = [d1_img,d2_img,d3_img,d4_img,d5_img,d6_img]
roll0_img = pygame.image.load("./graphics/Roll0.png").convert_alpha()
roll1_img = pygame.image.load("./graphics/Roll1.png").convert_alpha()
roll2_img = pygame.image.load("./graphics/Roll2.png").convert_alpha()
roll3_img = pygame.image.load("./graphics/Roll3.png").convert_alpha()
rollImages = [roll1_img,roll2_img,roll3_img,roll0_img]
accept_img = pygame.image.load("./graphics/Accept.png").convert_alpha()
accept_dis = pygame.image.load("./graphics/AcceptDis.png").convert_alpha()


new_button = button.Button(NEWX, NEWY, new_img, True)
quit_button = button.Button(QUITX, QUITY, quit_img, True)
roll_button = button.Button(ROLLX, ROLLY, roll1_img, True)
accept_button = button.Button(ACCEPTX, ACCEPTY, accept_dis, True)
continue_button = button.Button(WINDIALOGX + 110, WINDIALOGY + 120, continue_img, True)
winDialogBox = pygame.Rect(WINDIALOGX, WINDIALOGY, 400, 200)

font1 = pygame.font.SysFont("Tempus Sans ITC", 67)
font2 = pygame.font.SysFont("Tempus Sans ITC", 34)
font3 = pygame.font.SysFont("Tempus Sans ITC", 28)
font4 = pygame.font.SysFont("Tempus Sans ITC", 43, True)
font5 = pygame.font.SysFont("Tempus Sans ITC", 34, True)

# Main Program
def main():
    running = True
    while running:      # Each time through this loop represents an entire game           
        # Setup a new game here
        showWinDialogue = False
        rollNum = 1     # tracks number of rolls in a turn (max = 3)
        roundNum = 1    # tracks the 13 rounds in a game
        scotzeeNum = 0
        acceptEnable = False    # Enables/disables the Accept button
        boxSelected = False     # Indicates that a checkbox has been selected

        # Make the dice
        myDice = []
        for i in range(COLS):
            d = dice.Die(DX+DSPACE*i, DY, d0_img, 0, True)
            myDice.append(d)

        # Make the check boxes
        myBoxes = []
        ones = checkBox.CheckBox(C1X,R1Y,'Ones',CKBXCOL,CKBXDISCOL,True)
        myBoxes.append(ones)
        twos = checkBox.CheckBox(C1X,R2Y,'Twos',CKBXCOL,CKBXDISCOL,True)
        myBoxes.append(twos)
        threes = checkBox.CheckBox(C1X,R3Y,'Threes',CKBXCOL,CKBXDISCOL,True)
        myBoxes.append(threes)
        fours = checkBox.CheckBox(C1X,R4Y,'Fours',CKBXCOL,CKBXDISCOL,True)
        myBoxes.append(fours)
        fives = checkBox.CheckBox(C1X,R5Y,'Fives',CKBXCOL,CKBXDISCOL,True)
        myBoxes.append(fives)
        sixes = checkBox.CheckBox(C1X,R6Y,'Sixes',CKBXCOL,CKBXDISCOL,True)
        myBoxes.append(sixes)
        threeOfAKind = checkBox.CheckBox(C1X,R7Y,'Three of a Kind',CKBXCOL,CKBXDISCOL, True)
        myBoxes.append(threeOfAKind)
        fourOfAKind = checkBox.CheckBox(C1X,R8Y,'Four of a Kind',CKBXCOL,CKBXDISCOL, True)
        myBoxes.append(fourOfAKind)
        fullHouse = checkBox.CheckBox(C1X,R9Y,'Full House',CKBXCOL,CKBXDISCOL, True)
        myBoxes.append(fullHouse)
        smallStraight = checkBox.CheckBox(C1X,R10Y,'Small Straight',CKBXCOL,CKBXDISCOL, True)
        myBoxes.append(smallStraight)
        largeStraight = checkBox.CheckBox(C1X,R11Y,'Large Straight',CKBXCOL,CKBXDISCOL, True)
        myBoxes.append(largeStraight)
        chance = checkBox.CheckBox(C1X,R12Y,'Chance',CKBXCOL,CKBXDISCOL, True)
        myBoxes.append(chance)
        # Here's how to do this in one line
        myBoxes.append(checkBox.CheckBox(C1X,R13Y,'Scotzee!',CKBXCOL,CKBXDISCOL,True))

        gameOn = True   
        while gameOn:       # The main Pygame loop. Proceeds for 13 rounds or until Quit or New selected.
            # Draw the screen background
            screen.fill('cornsilk2')

            # Draw the game frame with border
            pygame.draw.rect(screen, 'lightgray', (ULEFTX, ULEFTY, BOUNDX, BOUNDY), 0, 35)
            pygame.draw.rect(screen, 'black', (ULEFTX, ULEFTY, BOUNDX, BOUNDY), 5, 35)

            # Draw Dice and Buttons
            for d in myDice:
                d.draw(screen)

            if roll_button.draw(screen):
                if rollNum <= 3:
                    rollDice(myDice, rollNum)
                    rollNum += 1
                    roll_button.image = rollImages[rollNum-1]

            # boxSelected processing goes here
            if (rollNum >= 2 and rollNum <= 4) and boxSelected:
                acceptEnable = True
                accept_button.image = accept_img
                # Draw the current score for the selected box; erase scores for unselected boxes
                for bx in myBoxes:
                    if not(bx.selected) and bx.enabled:
                        bx.score = 0
                        bx.drawScore = False
                    if bx.selected and bx.enabled:
                        if bx.label == 'Ones':
                            sc = dice.ones(myDice)
                            bx.score = sc
                        if bx.label == 'Twos':
                            sc = dice.twos(myDice)
                            bx.score = sc
                        if bx.label == 'Threes':
                            sc = dice.threes(myDice)
                            bx.score = sc
                        if bx.label == 'Fours':
                            sc = dice.fours(myDice)
                            bx.score = sc
                        if bx.label == 'Fives':
                            sc = dice.fives(myDice)
                            bx.score = sc
                        if bx.label == 'Sixes':
                            sc = dice.sixes(myDice)
                            bx.score = sc
                        if bx.label == 'Three of a Kind':
                            sc = dice.threeofakind(myDice)
                            bx.score = sc
                        if bx.label == 'Four of a Kind':
                            sc = dice.fourofakind(myDice)
                            bx.score = sc
                        if bx.label == 'Full House':
                            sc = dice.fullhouse(myDice)
                            bx.score = sc
                        if bx.label == 'Small Straight':
                            sc = dice.smallstraight(myDice)
                            bx.score = sc
                        if bx.label == 'Large Straight':
                            sc = dice.largestraight(myDice)
                            bx.score = sc
                        if bx.label == 'Chance':
                            sc = dice.chance(myDice)
                            bx.score = sc
                        if bx.label == 'Scotzee!':
                            sc = dice.scotzee(myDice)
                            bx.score = sc
                        bx.drawScore = True     # Will cause the checkbox score to be drawn

            if accept_button.draw(screen):
                if acceptEnable:        
                    # Reset roll and round, disable Accept button, reset Roll button, clear dice
                    roundNum += 1
                    rollNum = 1
                    acceptEnable = False
                    accept_button.image = accept_dis
                    roll_button.image = roll1_img
                    boxSelected = False
                    for d in myDice:
                        d.image = d0_img
                        d.selected = False
                    # Count number of Scotzee events for bonus calculation
                    if dice.scotzee(myDice) == 50:   
                        scotzeeNum += 1
                    # Check which box is selected and calculate score
                    for bx in myBoxes:
                        if bx.selected and bx.enabled:                       
                            if bx.label == 'Ones':
                                sc = dice.ones(myDice)
                                bx.score = sc
                            if bx.label == 'Twos':
                                sc = dice.twos(myDice)
                                bx.score = sc
                            if bx.label == 'Threes':
                                sc = dice.threes(myDice)
                                bx.score = sc
                            if bx.label == 'Fours':
                                sc = dice.fours(myDice)
                                bx.score = sc
                            if bx.label == 'Fives':
                                sc = dice.fives(myDice)
                                bx.score = sc
                            if bx.label == 'Sixes':
                                sc = dice.sixes(myDice)
                                bx.score = sc
                            if bx.label == 'Three of a Kind':
                                sc = dice.threeofakind(myDice)
                                bx.score = sc
                            if bx.label == 'Four of a Kind':
                                sc = dice.fourofakind(myDice)
                                bx.score = sc
                            if bx.label == 'Full House':
                                sc = dice.fullhouse(myDice)
                                bx.score = sc
                            if bx.label == 'Small Straight':
                                sc = dice.smallstraight(myDice)
                                bx.score = sc
                            if bx.label == 'Large Straight':
                                sc = dice.largestraight(myDice)
                                bx.score = sc
                            if bx.label == 'Chance':
                                sc = dice.chance(myDice)
                                bx.score = sc
                            if bx.label == 'Scotzee!':
                                sc = dice.scotzee(myDice)
                                bx.score = sc
                            bx.enabled = False      # Disable checkbox for future selection
                            bx.drawScore = True     # Will cause the checkbox score to be drawn
            
            # process scores
            uScore = 0
            bonus = 0
            lowerScore = 0
            for i in range(6):
                uScore = uScore + myBoxes[i].score
            if uScore >= 63:
                bonus = 35
            upperScore = uScore + bonus
            for i in range(6,13):
                lowerScore = lowerScore + myBoxes[i].score
            subTotal = upperScore + lowerScore
            if scotzeeNum >= 1:
                bonusScotzee = scotzeeNum - 1
            else:
                bonusScotzee = 0
            totalScore = subTotal + 100*(bonusScotzee)
            draw_text(screen, 'Upper Score:', font2, SCORECOL, SCOREX-SCOREGAP, SCOREY, False, True)
            draw_text(screen, str(uScore), font2, SCORECOL, SCOREX, SCOREY, False, True)
            draw_text(screen, 'Bonus:', font2, SCORECOL, SCOREX-SCOREGAP, SCOREY+ SCORESPACE*1, False, True)
            draw_text(screen, str(bonus), font2, SCORECOL, SCOREX, SCOREY + SCORESPACE*1, False, True)
            draw_text(screen, str(upperScore), font2, SCORECOL, SCOREX, SCOREY + SCORESPACE*2, False, True)
            draw_text(screen, 'Upper Total:', font2, SCORECOL, SCOREX-SCOREGAP, SCOREY+ SCORESPACE*2, False, True)
            draw_text(screen, str(lowerScore), font2, SCORECOL, SCOREX, SCOREY + SCORESPACE*3, False, True)
            draw_text(screen, 'Lower Total:', font2, SCORECOL, SCOREX-SCOREGAP, SCOREY+ SCORESPACE*3, False, True)
            draw_text(screen, str(subTotal), font5, SCORECOL, SCOREX, SCOREY + SCORESPACE*4, False, True)
            draw_text(screen, 'Subtotal:', font5, SCORECOL, SCOREX-SCOREGAP, SCOREY+ SCORESPACE*4, False, True)
            draw_text(screen, 'Bonus Scotzees', font2, 'slateblue4', SCOREX-SCOREGAP, SCOREY+ SCORESPACE*5, False, True)
            draw_text(screen, 'X 100:', font2, 'slateblue4', SCOREX-SCOREGAP, SCOREY+ SCORESPACE*6, False, True)
            draw_text(screen, str(bonusScotzee*100), font2, 'slateblue4', SCOREX, SCOREY + SCORESPACE*6, False, True)
            draw_text(screen, str(totalScore), font4, 'darkgreen', SCOREX, SCOREY + SCORESPACE*7+50, False, True)
            draw_text(screen, 'Total Score:', font4, 'darkgreen', SCOREX-SCOREGAP, SCOREY+ SCORESPACE*7+50, False, True)

            if new_button.draw(screen):
                gameOn = False
                roll_button.image = roll1_img
            
            if quit_button.draw(screen):
                running = False
                gameOn = False
            
            # Draw check boxes with radio button function. No changes if box is not enabled.
            for box in myBoxes:
                if box.draw(screen):
                    for b in myBoxes:
                        if b.enabled:
                            b.selected = False
                    box.selected = True
                    boxSelected = True

            # Draw round status and other text
            if roundNum <= 9:
                roundStr = '0'+str(roundNum)
                draw_text(screen, 'Round '+roundStr, font3, 'darkred', ROUNDX, ROUNDY, False)
            elif roundNum <=13:
                roundStr = str(roundNum)
                draw_text(screen, 'Round '+roundStr, font3, 'darkred', ROUNDX, ROUNDY, False)
            elif roundNum == 14:
                draw_text(screen, 'Game Over!', font2, 'navyblue', ROUNDX-50, ROUNDY, False)
                showWinDialogue = True
                roundNum = 15
                rollNum = 4
                roll_button.image = rollImages[3]
            elif roundNum == 15:
                draw_text(screen, 'Game Over!', font2, 'navyblue', ROUNDX-50, ROUNDY, False)

            draw_text(screen, 'Welcome to Scotzee!', font4, 'slateblue4', SCOTZEEX, SCOTZEEY, False)

            # Draw Win Dialogue
            if showWinDialogue:
                pygame.draw.rect(screen, 'cornsilk', winDialogBox, 0, 14)
                pygame.draw.rect(screen, 'black', winDialogBox, 2, 14)            
                draw_text(screen, 'Game Over!', font1, 'darkgreen', WINDIALOGX+30, WINDIALOGY+25, False)
                if continue_button.draw(screen):
                    showWinDialogue = False

            # Move things

            # Check Events
            events = pygame.event.get()
            moved = False
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        pass
                    if event.key == pygame.K_RIGHT:
                        pass
                    if event.key == pygame.K_DOWN:
                        pass    
                    if event.key == pygame.K_UP:
                        pass
                
                #if event.type == pygame.MOUSEBUTTONDOWN:
                #    pos = pygame.mouse.get_pos()
                #    looking = True

                if event.type == pygame.QUIT:
                    running = False
                    gameOn = False

            pygame.display.flip()

        # End of while gameOn

    # End of while running

# Functions
def draw_text(surface, text, font, text_col, x, y, outline, rjust=False):
    img = font.render(text, True, text_col)
    textRect = img.get_rect()
    if rjust:
        x = x - textRect.width
    textRect.topleft = (x - 5, y-5)
    textRect.height = textRect.height + 4
    textRect.width = textRect.width + 10
    if outline:
        pygame.draw.rect(screen,'white',textRect)
        pygame.draw.rect(screen,text_col,textRect, 2, 10)
    surface.blit(img, (x, y))

def rollDice(myD, rNum):
    for d in myD:
        if not(d.selected) or rNum == 1:
            val = choice([0,1,2,3,4,5])
            d.image = dieImages[val]
            d.value = val + 1
    # Scotzee Test - generates 5 of a kind on the third roll for testing
    #if rNum == 3:
    #    for d in myD:
    #        d.image = dieImages[4]
    #        d.value = 5

if __name__ == "__main__":
    main()