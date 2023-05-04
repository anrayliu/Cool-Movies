import pygame 
import sky 
from consts import *


class AccountButton:
    def __init__(self, x, y, index, data, graphics):
        self.rect = pygame.Rect(x, y, ACCOUNT_W, ACCOUNT_H)
        self.text_rect = pygame.Rect(self.rect.x, self.rect.bottom - 35, self.rect.w, 35)
        self.surf = pygame.Surface(self.text_rect.size)
        self.surf.set_alpha(RESULTS_ALPHA)
        self.index = index
        self.name, self.image = data
        
        try:
            graphics.images[self.image]
        except KeyError:
            self.image = "user"
        
    def update(self, events):
        if self.rect.collidepoint(events.mouse) and events.left_click:
            self.click = True 
        else:
            self.click = False
        
    def draw(self, graphics):
        graphics.draw(self.image, (0, 0), center=self.rect)
        pygame.draw.rect(graphics.surface, sky.BLACK, self.rect, 5)
        
        if self.name != None:
            graphics.surface.blit(self.surf, self.text_rect.topleft)
            graphics.write(self.name, (0, 0), center=self.text_rect, size=25)
