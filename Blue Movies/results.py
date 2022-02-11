import pygame 
import sky 
from consts import *
from card import Card
from math import ceil
from right_click import RightClick


class Results:
    def __init__(self, main):
        self.events = main.events 
        self.graphics = main.graphics
        self.inspector = main.inspector
        self.pickler = main.pickler
        self.win = self.graphics.surface
        
        self.rect = pygame.Rect(RESULTS_X, RESULTS_Y, RESULTS_W, RESULTS_H)
        self.surf = pygame.Surface(self.rect.size)
        self.surf.set_alpha(RESULTS_ALPHA)
        
        self.top_rect = pygame.Rect(self.rect.x, self.rect.y - CARD_H, self.rect.w, CARD_H)
        self.bottom_rect = pygame.Rect(self.rect.x, self.rect.bottom, self.rect.w, WIN_H - self.rect.bottom)
        
        self.rc = RightClick("")
        
        self.loaded = False
        
    def load(self, results):
        #[(name, image, url), (name, image, url)]
        if ceil(len(results) / CARD_COLUMNS) * (CARD_SPACING_Y + CARD_H) + CARD_SPACING_Y > RESULTS_H:
            self.have_slider = True
            self.rect.w = RESULTS_W
        else:
            self.have_slider = False 
            self.rect.w = RESULTS_W + SLIDER_W
        self.surf = pygame.transform.scale(self.surf, self.rect.size)
        
        card_spacing_x = (self.rect.w - CARD_W * CARD_COLUMNS) / (CARD_COLUMNS + 1)
        self.cards = []
        x = 0 
        y = 0
        for result in results:
            self.cards.append(Card(self.rect.x + card_spacing_x + (CARD_W + card_spacing_x) * x, self.rect.y + CARD_SPACING_Y + (CARD_H + CARD_SPACING_Y) * y, result, self.pickler.contains(result[2])))
            x += 1
            if x == CARD_COLUMNS:
                x = 0
                y += 1
                
        if self.have_slider:
            self.slider = sky.VerticalSlider(self.rect.right, self.rect.y, SLIDER_W, self.rect.h, range=(0, self.cards[-1].img_rect.y + CARD_SPACING_Y + CARD_H - self.rect.y - self.rect.h))
            
        self.loaded = True #update and draw only called if loaded
        
    def update(self):
        if self.have_slider:
            if self.rect.collidepoint(self.events.mouse):
                self.slider.set_drag_pos(self.slider.drag_rect.y - self.events.wheel * WHEEL_SENSITIVITY)
            self.slider.update(self.events)
            value = self.slider.value
        else:
            value = 0
            
        self.rc.update(self.events)
        if self.rc.click:
            if self.rc.button.text == "Remove from list":
                self.inspector.pickler.remove_title(self.rc.data[0])
            else:
                self.inspector.pickler.add_title(self.rc.data[0], "N/A", self.rc.data[1])
            self.rc.data = None
            self.events.left_click = None #prevent clicking stuff behind
        elif self.events.wheel != 0 or self.events.left_click:
            self.rc.data = None    
                        
        for card in self.cards:
            card.update(self.events, value)
            if self.events.right_click and card.img_rect.collidepoint(self.events.mouse):
                if self.pickler.contains(card.link):
                    text = "Remove from list"
                else:
                    text = "Add to list"
                self.rc.button.rect.topleft = self.events.mouse 
                self.rc.button.text = text
                self.rc.data = (card.text, card.link)
            elif card.click and self.top_rect.collidepoint(self.events.mouse) == False and self.bottom_rect.collidepoint(self.events.mouse) == False:
                self.inspector.load(card.link)
        
    def draw(self):
        self.win.blit(self.surf, self.rect.topleft) 
        if self.have_slider:
            self.slider.draw(self.graphics)
            
        top_subsurf = self.win.subsurface(self.top_rect).convert()
        bottom_subsurf = self.win.subsurface(self.bottom_rect).convert()
        
        for card in self.cards:
            card.draw(self.graphics)
            
        self.win.blit(top_subsurf, self.top_rect.topleft)
        self.win.blit(bottom_subsurf, self.bottom_rect.topleft)
        
        self.rc.draw(self.graphics)