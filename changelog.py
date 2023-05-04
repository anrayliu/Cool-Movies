import pygame
import sky 
from consts import *


class Changelog:
    def __init__(self, main):
        self.events = main.events
        self.graphics = main.graphics 
        self.pickler = main.pickler
        self.win = self.graphics.surface
        self.main = main #used to switch locations
        
        self.surf = pygame.Surface((DISPLAY_W - CHANGELOG_BORDER_SIZE * 2, DISPLAY_H - CHANGELOG_BORDER_SIZE * 2))
        self.surf.set_alpha(CHANGELOG_INNER_ALPHA)
        self.rect = self.surf.get_rect(topleft=(DISPLAY_X + CHANGELOG_BORDER_SIZE, DISPLAY_Y + CHANGELOG_BORDER_SIZE))
        self.horizontal_surf = pygame.Surface((DISPLAY_W, CHANGELOG_BORDER_SIZE))
        self.horizontal_surf.set_alpha(CHANGELOG_OUTER_ALPHA)
        self.vertical_surf = pygame.Surface((CHANGELOG_BORDER_SIZE, self.rect.h))
        self.vertical_surf.set_alpha(CHANGELOG_OUTER_ALPHA)
        
        self.lines = self.pickler.get_changelog()
        
        self.back_button = sky.Button(DISPLAY_X + DISPLAY_W + WIN_MARG, DISPLAY_Y, BB_W, BB_H, "Back", font="font", font_size=25, highlight="light blue")
        
        if len(self.lines) * (CHANGELOG_FONT_SIZE + 15) + DISPLAY_MARG * 2 > self.rect.h:
            self.have_slider = True 
            self.slider = sky.VerticalSlider(DISPLAY_X + DISPLAY_W - SLIDER_W - CHANGELOG_BORDER_SIZE, DISPLAY_Y + CHANGELOG_BORDER_SIZE, SLIDER_W, self.surf.get_height(), range=(0, CHANGELOG_BORDER_SIZE + len(self.lines) * (CHANGELOG_FONT_SIZE + 15) - self.rect.h))
        else:
            self.have_slider = False                                                                                               
        
    def update(self):
        if self.have_slider:
            self.slider.update(self.events)
            
        self.back_button.update(self.events)
        if self.back_button.click:
            self.main.location = "display"
        
    def draw(self):
        self.graphics.draw("wallpaper", (0, 0))
        self.graphics.write(NAME, (WIN_MARG, WIN_MARG / 2), colour="black", size=80, font="font")
        self.graphics.write(NAME, (WIN_MARG + 10, WIN_MARG / 2), size=80, font="font")
        
        topsurf = self.win.subsurface(DISPLAY_X, DISPLAY_Y, DISPLAY_W, CHANGELOG_BORDER_SIZE).convert()
        bottomsurf = self.win.subsurface(DISPLAY_X, self.rect.bottom, DISPLAY_W, CHANGELOG_BORDER_SIZE).convert()
        
        self.win.blit(self.vertical_surf, (DISPLAY_X, self.rect.y))
        self.win.blit(self.vertical_surf, (self.rect.right, self.rect.y))
        self.win.blit(self.surf, self.rect.topleft)
        
        if self.have_slider:
            if self.rect.collidepoint(self.events.mouse):
                self.slider.set_drag_pos(self.slider.drag_rect.y - self.events.wheel * WHEEL_SENSITIVITY)
            scroll = self.slider.value 
            self.slider.draw(self.graphics)
        else:
            scroll = 0
        for number, line in enumerate(self.lines):
            y = self.rect.y - scroll + DISPLAY_MARG + number * (CHANGELOG_FONT_SIZE + 15)
            if y < self.rect.bottom and y + CHANGELOG_FONT_SIZE + 15 > self.rect.y:
                self.graphics.write(line, (self.rect.x + DISPLAY_MARG, y))
                
        self.win.blit(topsurf, (DISPLAY_X, DISPLAY_Y))
        self.win.blit(bottomsurf, (DISPLAY_X, self.rect.bottom))
        self.win.blit(self.horizontal_surf, (DISPLAY_X, DISPLAY_Y))
        self.win.blit(self.horizontal_surf, (DISPLAY_X, self.rect.bottom))
        
        self.back_button.draw(self.graphics)