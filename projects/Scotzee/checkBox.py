import pygame

# Check Box Class
class CheckBox():
    def __init__(self, x, y, label, col, disCol, enabled):
        self.xpos = x
        self.ypos = y
        self.label = label
        self.enabled = enabled
        self.col = col
        self.disCol = disCol
        self.selected = False    
        self.score = 0          # Place the score here during game play?
        self.drawScore = False
      
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