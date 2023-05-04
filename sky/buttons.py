import pygame
from sky.tools import get_colour


class Button:
    def __init__(self, x, y, w, h, text, colour="black", highlight="yellow", font="arial", font_size="30", font_colour="white", center=None):
        if center != None:
            if center[3] != 0:
                y = center[1] + center[3]/2 - h/2
            if center[2] != 0:
                x = center[0] + center[2]/2 - w/2
        self.rect = pygame.Rect(x, y, w, h)
            
        self.text = text
        self.font = font
        self.font_size = font_size
        self.font_colour = get_colour(font_colour)
        self.colour = get_colour(colour)
        self.highlight = get_colour(highlight)
        
        self.click = False
        self.hover = False
        
    def update(self, events):
        self.click = False
        if self.rect.collidepoint(events.mouse):
            self.hover = True
            if events.left_click:
                self.click = True 
        else:
            self.hover = False
        
    def draw(self, graphics):
        if self.hover:
            colour = self.highlight
        else:
            colour = self.colour
        pygame.draw.rect(graphics.surface, colour, self.rect)
        graphics.write(self.text, (0, 0), center=self.rect, font=self.font, size=self.font_size, colour=self.font_colour)