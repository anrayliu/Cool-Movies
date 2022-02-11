import pygame
from sky.tools import get_colour


class Slider:
    def __init__(self, x, y, w, h, range, colour, dragger_colour, center):
        self.value = 0
        self.slider_rect = pygame.Rect(x, y, w, h)
        if center != None:
            if center[3] != 0:
                self.slider_rect.y = center[1] + center[3]/2 - self.slider_rect.h/2
            if center[2] != 0:
                self.slider_rect.x = center[0] + center[2]/2 - self.slider_rect.w/2
        self.drag = None
        self.colour = get_colour(colour)
        self.dragger_colour = get_colour(dragger_colour)
        
        self.range = range
        self.new_range = (0, self.range[1] - self.range[0])
        
    def draw(self, graphics):
        pygame.draw.rect(graphics.surface, self.colour, self.slider_rect)
        pygame.draw.rect(graphics.surface, self.dragger_colour, self.drag_rect)
        
        
class HorizontalSlider(Slider):
    def __init__(self, x, y, w, h, range=(0, 100), colour="gray", dragger_colour="black", center=None):
        super(HorizontalSlider, self).__init__(x, y, w, h, range, colour, dragger_colour, center)
        self.drag_rect = pygame.Rect(self.slider_rect[0], self.slider_rect[1], h, h)
        
        self.min = self.slider_rect.x
        self.max = self.slider_rect.x + self.slider_rect.w - self.slider_rect.h
        
        self.range_ratio = self.new_range[1] / (self.slider_rect.w - self.drag_rect.w)
        
    def update(self, events):
        if events.mouse_held[0]:
            if self.drag != None:
                self.set_drag_pos(events.x - self.drag)
            elif self.drag_rect.collidepoint(events.mouse):
                self.drag = events.x - self.drag_rect.x
        else:
            self.drag = None
        
    def set_drag_pos(self, x):
        self.drag_rect.x = x
        if self.drag_rect.x > self.max:
            self.drag_rect.x = self.max 
        elif self.drag_rect.x < self.min:
            self.drag_rect.x = self.min
            
        self.value = int((self.drag_rect.x - self.slider_rect.x) * self.range_ratio) + self.range[0] 

        
class VerticalSlider(Slider):
    def __init__(self, x, y, w, h, range=(0, 100), colour="gray", dragger_colour="black", center=None):
        super(VerticalSlider, self).__init__(x, y, w, h, range, colour, dragger_colour, center)
        self.drag_rect = pygame.Rect(self.slider_rect[0], self.slider_rect[1], w, w)
        
        self.min = self.slider_rect.y
        self.max = self.slider_rect.y + self.slider_rect.h - self.slider_rect.w
        
        self.range_ratio = self.new_range[1] / (self.slider_rect.h - self.drag_rect.h)
        
    def update(self, events):
        if events.mouse_held[0]:
            if self.drag != None:
                self.set_drag_pos(events.y - self.drag)
            elif self.drag_rect.collidepoint(events.mouse):
                self.drag = events.y - self.drag_rect.y
        else:
            self.drag = None
                    
    def set_drag_pos(self, y):
        self.drag_rect.y = y
        if self.drag_rect.y > self.max:
            self.drag_rect.y = self.max 
        elif self.drag_rect.y < self.min:
            self.drag_rect.y = self.min
            
        self.value = int((self.drag_rect.y - self.slider_rect.y) * self.range_ratio) + self.range[0] 