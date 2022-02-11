import pygame 
import sky 
from consts import *


class TrayButton:
    def __init__(self, x, y, img):
        self.x, self.y =  x, y
        self.img = img
        self.surf = pygame.Surface((TRAY_B_SIZE, TRAY_B_SIZE))
        self.rect = self.surf.get_rect(topleft=(x, y))
        self.surf.set_alpha(TRAY_ALPHA)
        
    def update(self, events):
        self.click = False
        if self.rect.collidepoint(events.mouse):
            self.surf.set_alpha(TRAY_HOVER_ALPHA)
            if events.left_click:
                self.click = True
        else:    
            self.surf.set_alpha(TRAY_ALPHA)
            
    def draw(self, graphics):
        graphics.surface.blit(self.surf, self.rect.topleft)
        graphics.draw(self.img, (0, 0), center=self.rect, size=(TRAY_B_SIZE, TRAY_B_SIZE))