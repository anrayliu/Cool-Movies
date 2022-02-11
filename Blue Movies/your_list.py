import pygame
import sky 
from consts import *
from list_button import ListButton
from right_click import RightClick


class YourList:
    def __init__(self, main):
        self.events = main.events
        self.graphics = main.graphics 
        self.inspector = main.inspector
        self.pickler = main.pickler
        self.win = self.graphics.surface
        
        self.rect = pygame.Rect(LOCATIONS_X, LOCATIONS_Y, LOCATIONS_W, LOCATIONS_H)
        self.surf = pygame.Surface(self.rect.size)
        self.surf.set_alpha(RESULTS_ALPHA)
                
        self.top_rect = pygame.Rect(self.rect.x, self.rect.y - LB_H, self.rect.w, LB_H)
        self.bottom_rect = pygame.Rect(self.rect.x, self.rect.bottom, self.rect.w, LB_H)
        
        self.rc = RightClick("")
                
    def load(self):        
        if len(self.pickler.titles) * LB_H > LOCATIONS_H:
            self.have_slider = True
            self.rect.w = LOCATIONS_W - SLIDER_W
        else:
            self.have_slider = False
            self.rect.w = LOCATIONS_W
        self.surf = pygame.transform.scale(self.surf, self.rect.size)
                
        self.buttons = []        
        for num, title in enumerate(self.pickler.titles):
            self.buttons.append(ListButton(self.rect.x, self.rect.y + LB_H * num, self.rect.w, LB_H, title, self.pickler.data[num]))
        
        if self.have_slider:
            self.slider = sky.VerticalSlider(self.rect.right, self.rect.y, SLIDER_W, self.rect.h, range=(0, self.buttons[-1].rect.y + LB_H - self.rect.y - self.rect.h))
        
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
                self.pickler.remove_title(self.rc.data[0])
            else:
                self.pickler.add_title(self.rc.data[0], "N/A", self.rc.data[1])
            self.rc.data = None
            self.events.left_click = None
            self.load()
        elif self.events.wheel != 0 or self.events.left_click:
            self.rc.data = None  
                            
        for button in self.buttons:
            button.update(self.events, value)
            if self.events.right_click and button.rect.collidepoint(self.events.mouse):
                if self.pickler.contains(button.link):
                    text = "Remove from list"
                else:
                    text = "Add to list"
                self.rc.button.rect.topleft = self.events.mouse 
                self.rc.button.text = text
                self.rc.data = (button.text, button.link)
            elif button.click and self.top_rect.collidepoint(self.events.mouse) == False and self.bottom_rect.collidepoint(self.events.mouse) == False:
                self.inspector.load(button.link)                
        
    def draw(self):
        if self.buttons != []:
            self.win.blit(self.surf, self.rect.topleft)
            if self.have_slider:
                self.slider.draw(self.graphics)
            
            top_subsurf = self.win.subsurface(self.top_rect).convert()
            bottom_subsurf = self.win.subsurface(self.bottom_rect).convert()
            
            for button in self.buttons:
                button.draw(self.graphics)
                
            self.win.blit(top_subsurf, self.top_rect.topleft)
            self.win.blit(bottom_subsurf, self.bottom_rect.topleft)
            
            self.rc.draw(self.graphics)
        else:
            self.graphics.write("Your list is empty", (0, 0), center=LOCATIONS_RECT, font="font")