import pygame 
import sky 
from consts import *


class Card:
    def __init__(self, x, y, info, watched):
        self.img_rect = pygame.Rect(x, y, CARD_W, IMG_H)
        self.text_rect = pygame.Rect(x, y + IMG_H, CARD_W, CARD_H - IMG_H)
        self.text, self.surf, self.link = info
        self.star_surf = pygame.Surface((WATCHED_STAR_SIZE, WATCHED_STAR_SIZE))
        self.star_surf.set_alpha(STAR_ALPHA)
        self.y = y
        
        self.showing = False
        self.watched = watched
        
    def update(self, events, scroll):
        self.img_rect.y = self.y - scroll
        self.text_rect.y = self.img_rect.bottom
        self.click = False
        if self.text_rect.bottom > RESULTS_Y and self.img_rect.y < RESULTS_Y + RESULTS_H:
            self.showing = True
            if self.img_rect.collidepoint(events.mouse) and events.left_click:
                self.click = True 
        else:
            self.showing = False
        
    def draw(self, graphics):
        if self.showing:
            graphics.surface.blit(self.surf, self.img_rect.topleft)
            if len(self.text) > CARD_TITLE_LENGTH:
                text = self.text[:CARD_TITLE_LENGTH] + "..."
            else:
                text = self.text
            graphics.write(text, (0, 0), center=self.text_rect, size=12)
            
            if self.watched:
                graphics.surface.blit(self.star_surf, self.img_rect.topleft)
                graphics.draw("star", self.img_rect.topleft, size=(WATCHED_STAR_SIZE, WATCHED_STAR_SIZE))