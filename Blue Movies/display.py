import pygame 
import sky
from consts import * 
from search import Search 
from your_list import YourList
from button import Button
from random import randrange, shuffle
from tray import Tray
from math import sin 


class Display:
    def __init__(self, main):
        self.events = main.events 
        self.graphics = main.graphics
        self.win = self.graphics.surface
        self.inspector = main.inspector 
        self.scraper = main.scraper
        
        self.wps = WALLPAPERS.copy()
        if self.wps == []:
            self.wps = ["wallpaper"]
        shuffle(self.wps)
        self.wp = self.wps[randrange(len(self.wps))]
        if len(self.wps) > 1:
            try:
                self.other_wp = self.wps[self.wps.index(self.wp) + 1]
            except IndexError:
                self.other_wp = self.wps[0]
        else:
            self.other_wp = None
        self.wp_switching = False
        self.wp_timer = 0 #for sin smooth transitioning
        self.wpx = 0
        
        self.surf = pygame.Surface((DISPLAY_W, DISPLAY_H))
        self.surf.set_alpha(DISPLAY_ALPHA)
        
        self.buttons = [Button(DISPLAY_X + i * BUTTON_W, DISPLAY_Y, BUTTONS[i]) for i in range(len(BUTTONS))]
        self.locations = {"Search":Search(main),
                          "Your list":YourList(main)}
        self.location = "Search"
        
        self.tray = Tray(main)
                        
    def update(self):
        if self.other_wp != None:
            if self.wp_switching:
                self.wp_timer += WP_SPEED
                self.wpx = sin(self.wp_timer) * WIN_W
                if round(self.wpx) == WIN_W:
                    self.wp_switching = False
                    self.wp = self.other_wp
                    self.wp_timer = 0
                    self.wpx = 0
                    try:
                        self.other_wp = self.wps[self.wps.index(self.wp) + 1]
                    except IndexError:
                        self.other_wp = self.wps[0]
            elif self.events.input_name == KEY_CHANGE_WP:
                self.wp_switching = True

        for button in self.buttons:
            button.update(self.events)
            if button.click and button.text != self.location and self.scraper.running == False:
                self.location = button.text
                self.inspector.active = False
                self.scraper.reset()
                    
        if self.inspector.active:
            self.inspector.update()
        else:
            self.locations[self.location].update()
            
        self.tray.update()
                                
    def draw(self):
        if self.wp_switching:
            self.win.blit(self.graphics.images[self.wp].subsurface(self.wpx, 0, WIN_W - self.wpx, WIN_H).convert(), (self.wpx, 0))
            self.win.blit(self.graphics.images[self.other_wp].subsurface(WIN_W - self.wpx, 0, self.wpx, WIN_H).convert(), (0, 0))
        else:
            self.graphics.draw(self.wp, (0, 0))
            
        self.graphics.write(NAME, (WIN_MARG, WIN_MARG / 2), colour="black", size=80, font="font")
        self.graphics.write(NAME, (WIN_MARG + 10, WIN_MARG / 2), size=80, font="font")
        self.win.blit(self.surf, (DISPLAY_X, DISPLAY_Y))
        
        for button in self.buttons:
            button.draw(self.graphics)
            
        if self.inspector.active:
            self.inspector.draw()
        else:
            self.locations[self.location].draw()
            
        self.tray.draw()