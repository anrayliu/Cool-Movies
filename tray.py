import pygame 
import sky 
from consts import * 
from tray_button import TrayButton


class Tray:
    def __init__(self, main):
        self.events = main.events 
        self.graphics = main.graphics 
        self.win = main.win
        self.main = main
        
        self.graphics.images["quit"] = pygame.transform.rotate(self.graphics.images["add"], 45)
        
        self.rect = pygame.Rect(WIN_W - TRAY_W, 0, TRAY_W, TRAY_H)
        self.buttons = [TrayButton(WIN_W - TRAY_B_SIZE, 0, "quit"), 
                        TrayButton(WIN_W - TRAY_B_SIZE * 2, 0, "user"),
                        TrayButton(WIN_W - TRAY_B_SIZE * 3, 0, "log")]
                        
        self.active = False
        
    def update(self):
        if self.rect.collidepoint(self.events.mouse):
            self.active = True 
            
            for button in self.buttons:
                button.update(self.events)
                if button.click:
                    if button.img == "quit":
                        self.main.close()
                    elif button.img == "user":
                        self.main.location = "accounts"
                    elif button.img == "log":
                        self.main.location = "changelog"
                        
        else:
            self.active = False
                        
    def draw(self):
        if self.active:
            for button in self.buttons:
                button.draw(self.graphics)