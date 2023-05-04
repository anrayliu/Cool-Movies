import pygame
import sky
from consts import *
from display import Display
from accounts import Accounts
from pickler import Pickler
from changelog import Changelog
from inspector import Inspector
from scraper import Scraper
from os.path import exists
from os import rmdir, remove
pygame.init()


class Main:
    def __init__(self):
        self.win = pygame.display.set_mode(WIN_SIZE, pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(NAME)
        
        self.events = sky.Events()
        self.graphics = sky.Graphics(self.win)
        
        self.graphics.load_folder(P_WP, WIN_SIZE)
        self.graphics.load_folder(P_AVATARS, (ACCOUNT_W, ACCOUNT_H))
        self.graphics.load_folder(P_FOLDER, {"search":(SB_R, SB_R),
                                             "add":(ACCOUNT_W / 2, ACCOUNT_H / 2),
                                             "unknown":(ACCOUNT_W / 2, ACCOUNT_H / 2),
                                             "wallpaper":WIN_SIZE,
                                             "user":(ACCOUNT_W, ACCOUNT_H),
                                             "arrow":(EB_W, EB_H)})
                                             
        self.pickler = Pickler()
        self.scraper = Scraper()
        self.inspector = Inspector(self)
        
        self.locations = {"display":Display(self), 
                          "accounts":Accounts(self),
                          "changelog":Changelog(self)}
        self.location = "accounts"
        
        self.pickler.list = self.locations["display"].locations["Your list"]
            
    def run(self):
        while True:
            self.events.update()
            if self.events.quit or self.events.input_name == "escape":
                self.close()
            self.clock.tick(60)
            
            if pygame.display.get_active():
                location = self.locations[self.location]
                location.update()
                location.draw()
                                
                pygame.display.update()
                
    def close(self):
        if exists(P_TEMP):
            try:
                remove(P_HTML)
            except FileNotFoundError:
                pass
            rmdir(P_TEMP)
        sky.close()

    
if __name__ == "__main__":
    Main().run()