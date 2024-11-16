import pygame

#button class
class Button():
    def __init__(self, x, y, image, enabled):
        self.xpos = x
        self.ypos = y
        self.image = image
        self.rect =  self.image.get_rect()
        self.rect.topleft = (x, y)
        self.enabled = enabled
        self.clicked = False

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

#peg class
class Peg():
    def __init__(self, x, y, radius, color, borderWidth):
        self.xpos = x
        self.ypos = y
        self.color = color
        self.radius = radius
        self.borderWidth = borderWidth
        #self.rect = pygame.rect.Rect(self.xpos, self.ypos, self.radius, self.radius)
        self.clicked = False

    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()

        pygame.draw.circle(surface, self.color, (self.xpos, self.ypos), self.radius, self.borderWidth)
        pygame.draw.circle(surface, 'black',(self.xpos, self.ypos), self.radius, 1) 

class ActivePeg():
    def __init__(self, x, y, radius, color, borderWidth):
        self.xpos = x
        self.ypos = y
        self.color = color
        self.radius = radius
        self.rect = pygame.Rect(self.xpos - self.radius, self.ypos-self.radius, 2*self.radius, 2*self.radius)
        self.borderWidth = borderWidth
        self.selected = False
        self.clicked = False

    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        pygame.draw.circle(surface, self.color, (self.xpos, self.ypos), self.radius, self.borderWidth)
        pygame.draw.circle(surface, 'black',(self.xpos, self.ypos), self.radius, 1)

        return action
    
class ActiveBlock():
    def __init__(self, x, y, width, height, color, borderWidth):
        self.xpos = x
        self.ypos = y
        self.color = color
        self.width = width
        self.height = height
        self.borderWidth = borderWidth
        self.rect = pygame.rect.Rect(self.xpos, self.ypos, self.width, self.height)
        self.selected = False       # Manage selected state outside of object so I can control a group
        self.clicked = False

    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        pygame.draw.rect(surface, self.color, self.rect, self.borderWidth)
        pygame.draw.rect(surface, 'black', self.rect, 1)
        if self.selected:
            pygame.draw.rect(surface, 'cyan', self.rect, 4)

        return action