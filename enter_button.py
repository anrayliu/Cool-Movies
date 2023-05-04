import pygame 
import sky 
from consts import *


class EnterButton:
    def __init__(self):
        self.surf = pygame.Surface((EB_W, EB_H), pygame.SRCALPHA)
        self.rect = self.surf.get_rect(y=WIN_CENTER_Y + ACCOUNT_H / 2 + DISPLAY_MARG * 2)
        
        self.active = True
        
    def update(self, events):
        self.click = False
        if self.rect.collidepoint(events.mouse) and events.left_click:
            self.click = True
            
    def draw(self, graphics):
        if self.active:
            alpha = 255 
        else:
            alpha = INACTIVE_ALPHA
        sky.draw_round_rect(self.surf, (0, 0, 0, alpha), (0, 0, self.rect.w, self.rect.h), SB_R)
        graphics.surface.blit(self.surf, self.rect.topleft)
        graphics.draw("arrow", (0, 0), center=self.rect)
