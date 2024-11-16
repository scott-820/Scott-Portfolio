import pygame

#dice class
class Die():
    def __init__(self, x, y, image, value, enabled):
        self.xpos = x
        self.ypos = y
        self.image = image
        self.value = value
        self.rect =  self.image.get_rect()
        self.rect.topleft = (x, y)
        self.enabled = enabled
        self.selected = False   # Manage selected outside of the object
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

# Score calculators

def ones(myDce):
    total = 0
    for di in myDce:
        if di.value == 1:
            total = total + di.value
    return total

def twos(myDce):
    total = 0
    for di in myDce:
        if di.value == 2:
            total = total + di.value
    return total

def threes(myDce):
    total = 0
    for di in myDce:
        if di.value == 3:
            total = total + di.value
    return total

def fours(myDce):
    total = 0
    for di in myDce:
        if di.value == 4:
            total = total + di.value
    return total

def fives(myDce):
    total = 0
    for di in myDce:
        if di.value == 5:
            total = total + di.value
    return total

def sixes(myDce):
    total = 0
    for di in myDce:
        if di.value == 6:
            total = total + di.value
    return total

def threeofakind(myDce):
    lst = []
    for di in myDce:
        lst.append(di.value)
    threeTest = False
    for i in range(3):
        count1 = lst.count(lst[i])
        if count1 >= 3:
            threeTest = True
    if threeTest:
        total = 0
        for val in lst:
            total = total + val
        return total
    else:
        return 0

def fourofakind(myDce):
    lst = []
    for di in myDce:
        lst.append(di.value)
    threeTest = False
    for i in range(2):
        count1 = lst.count(lst[i])
        if count1 >= 4:
            threeTest = True
    if threeTest:
        total = 0
        for val in lst:
            total = total + val
        return total
    else:
        return 0

def fullhouse(myDce):               
    lst = []
    for di in myDce:
        lst.append(di.value)
    uniqueList = []
    for val in lst:
        if not(val in uniqueList):
            uniqueList.append(val)
    ulen = len(uniqueList)
    if ulen == 1 or (ulen == 2 and (lst.count(uniqueList[0])==2 or lst.count(uniqueList[0])==3)):
        return 25
    else:
        return 0

def smallstraight(myDce):
    lst = []
    for di in myDce:
        lst.append(di.value)
    on = 1 in lst
    tw = 2 in lst
    th = 3 in lst
    fo = 4 in lst
    fi = 5 in lst
    si = 6 in lst
    uniqueList = []     # Check for Scotzee
    fiveofakind = False
    for val in lst:
        if not(val in uniqueList):
            uniqueList.append(val)
    if len(uniqueList) == 1:
        fiveofakind = True
    if (on and tw and th and fo) or (tw and th and fo and fi) or (th and fo and fi and si) or fiveofakind:
        return 30
    else:
        return 0

def largestraight(myDce):
    lst = []
    for di in myDce:
        lst.append(di.value)
    on = 1 in lst
    tw = 2 in lst
    th = 3 in lst
    fo = 4 in lst
    fi = 5 in lst
    si = 6 in lst
    uniqueList = []     # Check for Scotzee
    fiveofakind = False
    for val in lst:
        if not(val in uniqueList):
            uniqueList.append(val)
    if len(uniqueList) == 1:
        fiveofakind = True
    if (on and tw and th and fo and fi) or (tw and th and fo and fi and si) or fiveofakind:
        return 40
    else:
        return 0

def chance(myDce):
    total = 0
    for di in myDce:
        total = total + di.value
    return total

def scotzee(myDce):
    val = myDce[0].value
    sctzee = True
    for d in myDce:
        if d.value != val:
            sctzee = False
    if sctzee:
        return 50
    else:
        return 0
