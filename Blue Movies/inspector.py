import pygame 
import sky 
from consts import *
from threading import Thread
from loading_circle import LoadingCircle 
from webbrowser import open as open_web


class Inspector:
    def __init__(self, main):
        self.events = main.events 
        self.graphics = main.graphics 
        self.pickler = main.pickler
        self.scraper = main.scraper
        self.win = self.graphics.surface
        
        self.lc = LoadingCircle(self.win)
        
        self.back_button = sky.Button(LOCATIONS_X, LOCATIONS_Y, BB_W, BB_H, "Back", highlight="light blue", font="font", font_size=25)
        self.rating_rect = pygame.Rect(INSPECTOR_BUTTONS_START[0] + INSPECTOR_BUTTON_W + INSPECTOR_BUTTON_SPACING * 2 + RATING_STAR_SIZE, INSPECTOR_BUTTONS_START[1], RATING_W, RATING_H)
        
        self.active = False
        
    def load(self, link):  #always called before update or draw
        self.loaded = False
        self.active = True
        
        self.scraper.running = True
        Thread(target=self.scraper.get_page, args=(link, )).start()
                
    def update(self):
        if self.scraper.running == False:
            self.back_button.update(self.events)
            if self.back_button.click:
                self.active = False
                
            if self.loaded:
                self.list_button.update(self.events)
                if self.list_button.click:
                    if self.list_button.text == "Remove from list":
                        self.pickler.remove_title(self.name)
                        self.list_button.text = "Add to list"
                    else:
                        self.rating = ""
                        self.pickler.add_title(self.name, "N/A", self.link)
                        self.list_button.text = "Remove from list"
                    
                self.url_button.update(self.events)
                if self.url_button.click:
                    open_web(self.link)
                    pygame.display.iconify()
                    
                if self.watch_link != None:
                    self.watch_button.update(self.events)
                    if self.watch_button.click:
                        with open(P_HTML, "w") as f:
                            f.write(f'<iframe id="iframe" src="{self.watch_link}" width="100%" height="100%" allowfullscreen=true frameborder="0"></iframe>')
                        open_web(P_HTML)
                        pygame.display.iconify()
                
                if self.list_button.text == "Remove from list":
                    if self.rating == "" and self.events.input_key != None and self.events.input_key.isdigit() and self.events.input_key != "0":
                        self.rating += self.events.input_key
                        self.pickler.change_rating(self.name, int(self.rating))
                        
                    elif self.events.input_name == "backspace":
                        self.rating = ""
                        self.pickler.change_rating(self.name, "N/A")
                        
                    elif self.rating == "1" and self.events.input_key == "0":
                        self.rating = "10"
                        self.pickler.change_rating(self.name, "10")
                        
                        
            elif self.scraper.got_info:    
                self.info = self.scraper.info
                self.scraper.reset()
                self.image = self.info.pop("image")
                self.link = self.info.pop("link")
                self.name = self.info.pop("name")
                self.watch_link = self.info.pop("watch")
                self.loaded = True
                if self.pickler.contains(self.link):
                    text = "Remove from list"
                    self.rating = self.pickler.get_rating(self.name)
                else:
                    text = "Add to list"
                self.list_button = sky.Button(INSPECTOR_BUTTONS_START[0], INSPECTOR_BUTTONS_START[1], INSPECTOR_BUTTON_W, INSPECTOR_BUTTON_H, text, highlight="light blue", font="font", font_size=25)
                self.url_button = sky.Button(self.list_button.rect.x, self.list_button.rect.bottom + INSPECTOR_BUTTON_SPACING, INSPECTOR_BUTTON_W, INSPECTOR_BUTTON_H, "Open on TMDB", highlight="light blue", font="font", font_size=25)
                if self.watch_link != None:    
                    self.watch_button = sky.Button(self.list_button.rect.x, self.url_button.rect.bottom + INSPECTOR_BUTTON_SPACING, INSPECTOR_BUTTON_W, INSPECTOR_BUTTON_H, "Watch now", highlight="light blue", font="font", font_size=25)
        
    def draw(self):
        if self.scraper.running:
            self.lc.draw()
        else:
            self.back_button.draw(self.graphics)
            
            if self.loaded:
                self.win.blit(self.image, (LOCATIONS_X, self.back_button.rect.bottom + DISPLAY_MARG))
                if len(self.name) > TITLE_LENGTH:
                    text = self.name[:TITLE_LENGTH] + "..."
                else:
                    text = self.name
                self.graphics.write(text, (self.back_button.rect.right + DISPLAY_MARG, 0), center=(0, self.back_button.rect.y, 0, self.back_button.rect.h), font="font")
                
                self.list_button.draw(self.graphics)
                self.url_button.draw(self.graphics)
                if self.watch_link != None:
                    self.watch_button.draw(self.graphics)
                
                for num, pair in enumerate(self.info.items()):
                    self.graphics.write(f"{pair[0]}: {pair[1]}", (self.url_button.rect.x, self.back_button.rect.bottom + DISPLAY_MARG + num * INFO_SPACING), size=20, return_info=True)
                    
                if self.list_button.text == "Remove from list":
                    self.graphics.draw("star", (self.url_button.rect.right + INSPECTOR_BUTTON_SPACING, INSPECTOR_BUTTONS_START[1]), size=(RATING_STAR_SIZE, RATING_STAR_SIZE))
                    sky.draw_round_rect(self.win, sky.BLACK, self.rating_rect, SEARCH_R)
                    self.graphics.write(self.rating, (0, 0), center=self.rating_rect)
                
            elif self.scraper.error != None:
                self.graphics.write(self.scraper.error, (0, 0), center=LOCATIONS_RECT, size=40, font="font")