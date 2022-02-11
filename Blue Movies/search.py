import pygame
import sky
from consts import *
from loading_circle import LoadingCircle
from threading import Thread
from search_button import SearchButton
from results import Results


class Search:
    def __init__(self, main):
        self.events = main.events
        self.graphics = main.graphics
        self.win = self.graphics.surface
        self.scraper = main.scraper
        
        self.lc = LoadingCircle(self.win)
                
        self.search = ""
        self.search_rect = pygame.Rect(LOCATIONS_X, LOCATIONS_Y, 0, SEARCH_H)
        self.search_button = SearchButton(LOCATIONS_X + LOCATIONS_W - SB_R, self.search_rect.center[1])
        
        self.search_type = "movie"
        self.dropdown_button = sky.Button(DD_X, DD_Y, DD_W, DD_H, self.search_type, highlight="light blue", font="font", font_size=25)
        self.dd_buttons = [sky.Button(DD_X, DD_Y + (i + 1) * DD_H, DD_W, DD_H, ["movie", "tv"][i], highlight="light blue", font="font", font_size=25) for i in range(2)]
        self.dropdown = False
        
        self.results = Results(main)
        
        self.backspace_timer = 0
        
    def update(self):
        if self.events.input_key != None:
            if self.events.input_name == "backspace" and len(self.search) > 0:
                self.search = self.search[:-1]
            elif self.events.input_name == "space":
                self.search += " "
            elif len(self.events.input_name) == 1:
                self.search += self.events.input_key
                
        if self.events.keys_held[pygame.K_BACKSPACE]:
            self.backspace_timer += 1
            if self.backspace_timer > BACKSPACE_THRESHOLD and self.backspace_timer % 2 == 0 and len(self.search) > 0:
                self.search = self.search[:-1]
        else:
            self.backspace_timer = 0
        
        w = self.graphics.fonts["font"]["30"].render(self.search, True, sky.BLACK).get_width()
        if self.search_rect.x + w + SEARCH_MARG > DD_X - DISPLAY_MARG:
            self.search = self.search[:-1]
            w = self.graphics.fonts["font"]["30"].render(self.search, True, sky.BLACK).get_width()
        self.search_rect.w = w + SEARCH_MARG
        
        self.dropdown_button.update(self.events)
        if self.dropdown_button.click:
            self.dropdown = 1 - self.dropdown
        if self.dropdown:
            self.search_button.active = False
            self.dropdown_button.text = ""
            for button in self.dd_buttons:
                button.update(self.events)
                if button.click:
                    self.dropdown = False 
                    self.search_type = button.text
                    self.dropdown_button.text = self.search_type
                    self.events.left_click = False #prevents clicking overlaps below dropdown list
        else:
            self.search_button.active = self.scraper.running == False
        
        self.search_button.update(self.events)
        if (self.search_button.click or self.events.input_name == "return") and self.search_button.active:
            self.scraper.running = True
            Thread(target=self.scraper.get_results, args=(self.search_type, self.search)).start()
            self.results.loaded = False #reset results data
        
        if self.results.loaded:
            self.results.update()
        elif self.scraper.got_info:
            self.results.load(self.scraper.info)
            self.scraper.reset()
        
    def draw(self):
        if self.search_rect.w < SEARCH_MIN_W:
            sky.draw_round_rect(self.win, sky.BLACK, (self.search_rect.x, self.search_rect.y, SEARCH_MIN_W, self.search_rect.h), SEARCH_R)
        else:
            sky.draw_round_rect(self.win, sky.BLACK, self.search_rect, SEARCH_R)
        self.graphics.write(self.search, (0, 0), center=self.search_rect, font="font")
        self.search_button.draw(self.graphics)
        
        if self.scraper.running:
            self.lc.draw()
        elif self.results.loaded:
            self.results.draw()
        elif self.scraper.error != None:
            self.graphics.write(self.scraper.error, (0, 0), center=LOCATIONS_RECT, size=40, font="font")
            
        self.dropdown_button.draw(self.graphics)
        if self.dropdown:
            for button in self.dd_buttons:
                button.draw(self.graphics)
