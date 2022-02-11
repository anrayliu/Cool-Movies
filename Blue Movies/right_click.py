import pygame 
import sky 
from consts import * 


class RightClick:
    def __init__(self, text):
        self.button = sky.Button(0, 0, INSPECTOR_BUTTON_W, INSPECTOR_BUTTON_H, text, highlight="light blue", font="font", font_size=25)
        self.data = None
        
    def update(self, events):
        self.click = None
        if self.data != None:
            self.button.update(events)
            self.click = self.button.click
        
    def draw(self, graphics):
        if self.data != None:
            self.button.draw(graphics)