import sky
from consts import *
from pygame import gfxdraw


class LoadingCircle:
    def __init__(self, win, x=LOCATIONS_CENTER_X, y=LOCATIONS_CENTER_Y):
        self.angle = 0 
        self.win = win 
        self.x, self.y = x, y
    
    def draw(self):
        self.angle -= LC_SPEED
        gfxdraw.aacircle(self.win, self.x, self.y, LC_R, sky.WHITE)
        gfxdraw.arc(self.win, self.x, self.y, LC_R, self.angle, self.angle + LC_ARC_SIZE, LC_COLOUR)
        