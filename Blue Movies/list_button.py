import pygame 
import sky 
from consts import *


class ListButton:
    def __init__(self, x, y, w, h, text, data):
        self.y = y 
        self.rect = pygame.Rect(x, y, w, h)
        self.surf = pygame.Surface(self.rect.size)
        self.text = text
        self.rating, self.link = data
        
        self.showing = False
        self.alpha = LIST_BUTTON_MIN_ALPHA
        
    def update(self, events, scroll):
        self.rect.y = self.y - scroll
        self.click = False
        if self.rect.bottom > LOCATIONS_Y and self.rect.top < LOCATIONS_Y + LOCATIONS_H:
            self.showing = True 
            if self.rect.collidepoint(events.mouse):
                self.alpha *= ALPHA_ACCEL
                if self.alpha > BUTTON_MAX_ALPHA:
                    self.alpha = BUTTON_MAX_ALPHA
                if events.left_click:
                    self.click = True
            else:
                self.alpha *= ALPHA_DEACCEL
                if self.alpha < LIST_BUTTON_MIN_ALPHA:
                    self.alpha = LIST_BUTTON_MIN_ALPHA

            self.surf.set_alpha(self.alpha)
        else:
            self.showing = False
        
    def draw(self, graphics):
        if self.showing:
            graphics.surface.blit(self.surf, self.rect.topleft)
            if len(self.text) > TITLE_LENGTH:
                text = self.text[:TITLE_LENGTH] + "..."
            else:
                text = self.text
            graphics.write(text, (self.rect.x + DISPLAY_MARG, 0), center=(0, self.rect.y, 0, self.rect.h), size=25, font="font")
            graphics.write(self.rating, (0, 0), size=25, center=(self.rect.right - DISPLAY_MARG - LIST_LAST_RECT_W, self.rect.y, LIST_LAST_RECT_W, self.rect.h))
            graphics.draw("star", (0, 0), size=(round(self.rect.h / 2), round(self.rect.h / 2)), center=(self.rect.right - DISPLAY_MARG - LIST_LAST_RECT_W * 2, self.rect.y, LIST_LAST_RECT_W, self.rect.h))