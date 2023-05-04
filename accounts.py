import pygame
import sky 
from consts import *
from account_button import AccountButton
from enter_button import EnterButton
from right_click import RightClick
from random import choice


class Accounts:
    def __init__(self, main):
        self.events = main.events
        self.graphics = main.graphics 
        self.pickler = main.pickler
        self.win = self.graphics.surface
        self.main = main #used to switch locations
        
        self.typing = False
        self.name = ""
        self.text_rect = pygame.Rect(0, 0, 0, 0)
        self.backspace_timer = 0
        
        self.rc = RightClick("Delete")
        self.enter_button = EnterButton()
        
        self.load()
        
    def load(self, making_new=False):
        data = self.pickler.get_accounts()
        length = len(data) + 1 * making_new
        if length == 0:
            length = 1
        elif length < MAX_ACCOUNTS:
            length += 1
            
        self.rect = pygame.Rect(0, 0, length * ACCOUNT_W + (length - 1) * DISPLAY_MARG + DISPLAY_MARG * 2, ACCOUNT_H + DISPLAY_MARG * 2)
        self.rect.x = WIN_CENTER_X - self.rect.w / 2
        self.rect.y = WIN_CENTER_Y - self.rect.h / 2
        self.surf = pygame.Surface(self.rect.size)
        self.surf.set_alpha(DISPLAY_ALPHA)
        
        made_new = False
        self.buttons = []
        for i in range(length):
            try:
                self.buttons.append(AccountButton(self.rect.x + DISPLAY_MARG + (ACCOUNT_W + DISPLAY_MARG) * i, self.rect.y + DISPLAY_MARG, i, data[i], self.graphics))
            except IndexError:
                if making_new and made_new == False:
                    temp_data = (None, "unknown")
                    made_new = True
                else:
                    temp_data = (None, "add")
                self.buttons.append(AccountButton(self.rect.x + DISPLAY_MARG + (ACCOUNT_W + DISPLAY_MARG) * i, self.rect.y + DISPLAY_MARG, i, temp_data, self.graphics))
                
    def update(self):
        if self.typing:
            if self.events.input_key != None:
                if self.events.input_name == "backspace" and len(self.name) > 0:
                    self.name = self.name[:-1]
                elif self.events.input_name == "space" and len(self.name) < MAX_NAME_LENGTH:
                    self.name += " "
                elif len(self.events.input_name) == 1 and len(self.name) < MAX_NAME_LENGTH:
                    self.name += self.events.input_key
                    
            if self.events.keys_held[pygame.K_BACKSPACE]:
                self.backspace_timer += 1
                if self.backspace_timer > BACKSPACE_THRESHOLD and self.backspace_timer % 2 == 0 and len(self.name) > 0:
                    self.name = self.name[:-1]
            else:
                self.backspace_timer = 0
                        
            w = self.graphics.fonts["font"]["30"].render(self.name, True, sky.BLACK).get_width() + SEARCH_MARG
            if w < SEARCH_MIN_W:
                w = SEARCH_MIN_W
            self.text_rect = pygame.Rect(WIN_CENTER_X - (w + DISPLAY_MARG + EB_W) / 2, self.rect.bottom + DISPLAY_MARG, w, SEARCH_H)
            self.enter_button.rect.x = self.text_rect.right + DISPLAY_MARG
            
            if self.name.replace(" ", "") == "":
                self.enter_button.active = False 
            else:
                self.enter_button.active = True

                self.enter_button.update(self.events)
                if self.enter_button.click or self.events.input_name == "return":
                    self.typing = False
                    avatars = AVATARS.copy()
                    if len(avatars) == 0:
                        avatar = "user"
                    else:
                        for button in self.buttons:
                            if button.image != "unknown" and button.image != "add":
                                avatars.pop(avatars.index(button.image))
                        avatar = choice(avatars)
                    self.pickler.add_account(self.name, avatar)
                    for button in self.buttons:
                        if button.image == "unknown":
                            button.image = avatar
                            button.name = self.name
                
        else:
            self.rc.update(self.events)
            if self.rc.click:
                self.pickler.remove_account(self.rc.data)
                self.rc.data = None
                self.events.left_click = None
                self.load()
            elif self.events.left_click:
                self.rc.data = None    
                                
            for button in self.buttons:
                button.update(self.events)
                if button.click:
                    if button.image == "add":
                        self.typing = True
                        self.name = ""
                        self.load(making_new=True)
                    else:
                        self.pickler.open_account(button.index)
                        self.main.location = "display"
                        self.main.locations["display"].locations["Your list"].load()
                elif self.events.right_click and button.rect.collidepoint(self.events.mouse) and button.image != "add":
                    self.rc.data = button.index
                    self.rc.button.rect.topleft = self.events.mouse
        
    def draw(self):
        self.graphics.draw("wallpaper", (0, 0))
        self.win.blit(self.surf, self.rect.topleft)
        
        self.graphics.write("Choose an account", (0, self.rect.y - DISPLAY_MARG - 61), center=(0, 0, WIN_W, 0), font="font", size=60, return_info=True)
        
        for button in self.buttons:
            button.draw(self.graphics)
            
        if self.typing:
            sky.draw_round_rect(self.win, sky.BLACK, self.text_rect, SEARCH_R)
            self.graphics.write(self.name, (0, 0), center=self.text_rect, font="font")
            self.enter_button.draw(self.graphics)
        else:
            self.rc.draw(self.graphics)