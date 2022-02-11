import pygame 
import sky 
from consts import *
from math import sqrt


class SearchButton:
    def __init__(self, x, y):
        self.x, self.y =  x, y #button center coordinates
        self.surf = pygame.Surface((SB_R * 2, SB_R * 2), pygame.SRCALPHA)
        self.rect = self.surf.get_rect(center=(self.x, self.y))
        
        self.active = True
        
    def update(self, events):
        self.click = False
        if self.active:
            if sqrt((events.x - self.x) ** 2 + (events.y - self.y) ** 2) < SB_R:
                if events.left_click:
                    self.click = True
            self.alpha = 255
        else:    
            self.alpha = INACTIVE_ALPHA
            
    def draw(self, graphics):
        pygame.draw.circle(self.surf, (0, 0, 0, self.alpha), (SB_R, SB_R), SB_R)
        graphics.surface.blit(self.surf, (self.x - SB_R, self.y - SB_R))
        graphics.draw("search", (0, 0), center=self.rect)