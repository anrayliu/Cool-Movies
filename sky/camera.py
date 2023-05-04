import pygame


class Camera:
    def __init__(self, size):
        self.x = 0
        self.y = 0
        self.w, self.h = size
        self.shake_cooldown = 0.9
        self.shakex = 0 
        self.shakey = 0
        self.following = None 
    
    def update(self):
        if not self.shakex == 0:
            self.shakex *= -self.shake_cooldown
            if abs(self.shakex) < 0.5:
                self.shakex = 0
        if not self.shakey == 0:
            self.shakey *= -self.shake_cooldown
            if abs(self.shakey) < 0.5:
                self.shakey = 0
        
        if self.following != None:
            self.x = -self.following.x + self.w/2 + self.shakex - self.following.width/2
            self.y = -self.following.y + self.h/2 + self.shakey - self.following.height/2
        else:
            self.x, self.y = self.shakex, self.shakey
            
    def shake(self, xamount, yamount):
        self.shakex = xamount
        self.shakey = yamount