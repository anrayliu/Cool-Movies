import pygame 
import random #randint
import math #radians, sin, cos
from sky.tools import get_colour


class LineParticle:
    def __init__(self, pos, angle=(0, 360), length=(20, 40), speed=(5, 15), colour="white", thickness=(5, 15)):
        self.x, self.y = pos 
        self.angle = math.radians(random.randint(-angle[1], -angle[0]))
        self.length = random.randint(length[0], length[1])
        self.speed = random.randint(speed[0], speed[1])
        self.thickness = random.randint(thickness[0] ,thickness[1])
        self.colour = get_colour(colour)
        self.delete = False
        
    def update(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        self.length -= 1
        self.thickness -= 1
        if self.length == 0 or self.thickness == 0:
            self.delete = True
        
    def draw(self, surface):
        pygame.draw.line(surface, self.colour, (self.x, self.y), (self.x + math.cos(self.angle) * self.length, self.y + math.sin(self.angle) * self.length), self.thickness)  
        
        
class CircleParticle:
    def __init__(self, pos, size=(5, 10), stroke=(5, 10), speed=(5, 10), colour="white"):
        self.x, self.y = pos
        self.speed = random.randint(speed[0], speed[1])
        self.stroke = random.randint(stroke[0], stroke[1])
        self.radius = random.randint(size[0], size[1])
        self.colour = get_colour(colour)
        self.delete = False
        
    def update(self):
        self.stroke -= 0.5
        if round(self.stroke) == 0:
            self.delete = True
        self.radius += self.speed
            
    def draw(self, surface):
        pygame.draw.circle(surface, self.colour, (self.x, self.y), self.radius, round(self.stroke))
        

class FallingParticle:
    def __init__(self, pos, size=(4, 8), angle=(60, 120), speed=(5, 10), colour="white", gravity=0.3):
        self.x, self.y = pos
        self.angle = math.radians(random.randint(-angle[1], -angle[0]))
        self.gravity = 0
        self.gravity_change = gravity
        self.speed = random.randint(speed[0], speed[1])
        self.size = random.randint(size[0], size[1])
        self.colour = get_colour(colour)
        self.delete = False
        
    def update(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        self.size -= 0.1
        if self.size < 0:
            self.delete = True
        self.y += self.gravity
        self.gravity += self.gravity_change
            
    def draw(self, surface):
        pygame.draw.circle(surface, self.colour, (self.x, self.y), self.size)