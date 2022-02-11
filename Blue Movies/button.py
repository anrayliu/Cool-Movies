import pygame 
import sky 
from consts import *


class Button:
    def __init__(self, x, y, text):
        self.rect = pygame.Rect(x, y, BUTTON_W, BUTTON_H)
        self.surf = pygame.Surface(self.rect.size)
        self.text = text
        
        self.alpha = BUTTON_MIN_ALPHA
        
    def update(self, events):
        self.click = False
        if self.rect.collidepoint(events.mouse):
            self.alpha *= ALPHA_ACCEL
            if self.alpha > BUTTON_MAX_ALPHA:
                self.alpha = BUTTON_MAX_ALPHA
            if events.left_click:
                self.click = True
        else:
            self.alpha *= ALPHA_DEACCEL
            if self.alpha < BUTTON_MIN_ALPHA:
                self.alpha = BUTTON_MIN_ALPHA
                
        self.surf.set_alpha(self.alpha)
            
    def draw(self, graphics):
        graphics.surface.blit(self.surf, self.rect.topleft)
        graphics.write(self.text, (0, 0), center=self.rect, font="font")