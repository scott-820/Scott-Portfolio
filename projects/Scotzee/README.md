# Scotzee
## A Familiar Dice Game with an Exceedingly Clever Name
Scotzee is a dice game where the player tries to maximize their score in a game of 13 rounds across 13 different scoring categories.
#### Watch a video demo of the project here: <https://youtu.be/xRx9d-cMRj8>
## To Do
* ~Add Best Score tracking, storage and user notification~
  
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
Game flow and logic is managed in this file, primarily within the main() function which implements a fairly standard pygame loop that repeatedly:
* Draws game elements to the screen
* Checks mouse-enabled elements for mouse clicks/selection, responding appropriately
* Checks for events (just pygame.QUIT in this program), responding appropriately

A pygame loop normally will handle movement of elements on the screen as well, however Scotzee has no moving elements to handle.
>**Note:** The graphics files used in scotzee.py are all located in the folder "./graphics"
#### settings.py:
This file contains the game settings and "constants". Use "from settings import *" to avoid the need to prefix "settings." to all items referenced from settings.py.
#### button.py:
This file contains several classes that I frequently use in game design -Button(), Peg(), ActivePeg() and ActiveBlock(). For Scotzee, only the Button() class is used.

The __init__() method is shown below and takes x and y integer screen positions, a pygame image for the face of the button and a boolean called "enabled" which enables/disables mouse selectivity:
```python
  def __init__(self, x, y, image, enabled):
      self.xpos = x
      self.ypos = y
      self.image = image
      self.rect =  self.image.get_rect()
      self.rect.topleft = (x, y)
      self.enabled = enabled
      self.clicked = False
```

The draw() method takes a pygame surface as an input and will draw the button's self.image at position self.x / self.y on that surface. The method employs a nice trick that I learned somewhere in the many YouTube videos that I consumed while studying pygame, which is that draw() not only draws the button on a surface, but it will also return True if the mouse position collides with the button being drawn and if the mouse left-button is being pressed at the time. Since draw() is normally within the pygame loop and frequently called, it can also be used to check for button mouse-overs and clicks as an alternative to processing mouse events in the event handler section of the pygame loop.  

This dual capability is repeated in the draw() methods for ActivePeg(), ActiveBlock() classes in the file "button.py", as well as in the Die() class in the file "dice.py" and the CheckBox() class in the file "checkBox.py". \(Maybe I should think about using class hierarchies and inheritance here, but will save that for another day...).  Here's the draw() method:
```python
  def draw(self, surface):
      action = False
      if self.enabled:
          pos = pygame.mouse.get_pos()
          if self.rect.collidepoint(pos):
              if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                  self.clicked = True
                  action = True
          if pygame.mouse.get_pressed()[0] == 0:
              self.clicked = False

      surface.blit(self.image, (self.rect.x, self.rect.y))

      return action
```
####  dice.py:
This file contains the class Die() which is used to manage and draw the dice in the Scotzee game.  The Die() class is very similar to the button class, but has an additional attribute called "self.selected" which when True will cause a cyan outline to be drawn around the Die object as part of the draw() method.  '\(Again, there seems to be an opportunity for inheritance here that should be explored.)
```python
class Die():
    def __init__(self, x, y, image, value, enabled):
        self.xpos = x
        self.ypos = y
        self.image = image
        self.value = value
        self.rect =  self.image.get_rect()
        self.rect.topleft = (x, y)
        self.enabled = enabled
        self.selected = False
        self.clicked = False

    def draw(self, surface):
        action = False
        if self.enabled:
            pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    self.clicked = True
                    self.selected = not(self.selected)
                    action = True
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

        surface.blit(self.image, (self.rect.x, self.rect.y))
        if self.selected:
            pygame.draw.rect(surface,'cyan',(self.rect.x, self.rect.y, self.rect.width, self.rect.height), 7, 25)

        return action
```
The various upper and lower half scoring category score calculator functions are also contained within "dice.py". Each function accepts a list of Die() objects and processes them with appropriate logic, returning an integer score value.  For example, the score calculator function that corresponds to the "Twos" scoring category is:
```python
def twos(myDce):  # myDce is a list of Die() objects
    total = 0
    for di in myDce:
        if di.value == 2:
            total += di.value
    return total
```
#### checkBox.py:
This file contains the CheckBox() class which is used to present the upper and lower half scoring categories on the game screen. Though similar in concept to Button() and Die() regarding dual management of draw and mouse-over/click handling, it is more complex in that it must also handle a "checkable" box image, a user defined label, optional score text, and two color selections - one used for the "selectable" state and another for the "not selectable" state.
```python
class CheckBox():
    def __init__(self, x, y, label, col, disCol, enabled):
        self.xpos = x
        self.ypos = y
        self.label = label
        self.enabled = enabled
        self.col = col          # Text color when checkbox is enabled
        self.disCol = disCol    # Text color when checkbox is disabled
        self.selected = False    
        self.score = 0          # The score value currently assigned to the checkbox  
        self.drawScore = False  # Init to False; logically managed externally by the user
      
    def draw(self, surface):
        drawCol = self.col
        if not(self.enabled):
            drawCol = self.disCol
        font = pygame.font.SysFont("Tempus Sans ITC", 30)
        font2 = pygame.font.SysFont("Tempus Sans ITC", 28)
        img = font.render(self.label, True, drawCol)
        scor = font2.render(str(self.score), True, 'black')
        boxRect = pygame.Rect(self.xpos, self.ypos+5, 15, 15)
        maskRect = img.get_rect()
        maskRect.topleft = (self.xpos, self.ypos)
        maskRect.width = maskRect.width + 20
        scoreRect = scor.get_rect()

        action = False
        pos = pygame.mouse.get_pos()
        if self.enabled:
            if maskRect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    self.clicked = True
                    self.selected = not(self.selected)
                    action = True
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
        pygame.draw.rect(surface,drawCol,boxRect, 2)
        pygame.draw.line(surface,'black', (self.xpos - 45, self.ypos + 20), (self.xpos - 5, self.ypos + 20), 1)
        if self.selected:
            pygame.draw.rect(surface,drawCol,boxRect)
        surface.blit(img, (self.xpos + 20, self.ypos-8))
        if self.drawScore:
            surface.blit(scor, (self.xpos - scoreRect.width - 7, self.ypos-8))

        return action
```


#### End README.md
