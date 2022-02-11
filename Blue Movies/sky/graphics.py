import pygame
import os #listdir, path.join, path.split
from sky.tools import get_colour


class Graphics:
    def __init__(self, surface):
        self.surface = surface
        self.font = "arial"
        
        self.images = {}
        self.resized_images = {}
        self.fonts = {"arial":{"30":pygame.font.SysFont("arial", 30)}}
        self.font_paths = {}
        
    def load_folder(self, dir, resize={}):
        for file in os.listdir(dir):
            if file.endswith(".ttf") or file.endswith(".otf"):
                self.load_font(os.path.join(dir, file))
            elif file.endswith(".png") or file.endswith(".jpg"):
                if file[:-4] in resize:
                    self.load_image(os.path.join(dir, file), resize[file[:-4]])
                elif not type(resize) is dict:
                    self.load_image(os.path.join(dir, file), resize)
                else:
                    self.load_image(os.path.join(dir, file))
    
    def load_font(self, path):
        head, tail = os.path.split(path)
        name = tail[:-4]
        self.font_paths[name] = path
        self.fonts[name] = {}
        self.fonts[name]["30"] = pygame.font.Font(path, 30)
        
    def load_image(self, path, dimensions=None):
        head, tail = os.path.split(path)
        img = pygame.image.load(path).convert_alpha()
        if dimensions != None:
            img = pygame.transform.scale(img, (int(dimensions[0]), int(dimensions[1])))
        self.images[tail[:-4]] = img
                
    def load_sysfont(self, font):
        self.fonts[font] = {}
        self.fonts[font]["30"] = pygame.font.SysFont(font, 30)
        
    def draw(self, picture, pos, angle=None, size=None, transparency=None, center=None, return_info=False):
        image = self.images[picture].copy()
        x, y = pos
        if size != None:
            if picture in self.resized_images:
                if str(size) in self.resized_images[picture]:
                    image = self.resized_images[picture][str(size)]
                else:
                    self.resized_images[picture][str(size)] = image = pygame.transform.scale(image, size)
            else:
                image = pygame.transform.scale(image, size)
                self.resized_images[picture] = {str(size):image}
        if angle != None:
            image = pygame.transform.rotate(image, angle)
            rect = image.get_rect(center=(x, y))
            x, y = rect.topleft
        if center != None:
            if center[3] != 0:
                y = center[1] + center[3]/2 - image.get_height()/2
            if center[2] != 0:
                x = center[0] + center[2]/2 - image.get_width()/2
        if transparency != None:
            image.set_alpha(transparency)
        self.surface.blit(image, (x, y))
        if return_info:
            return (x, y, image.get_width(), image.get_height())

    def write(self, text, pos, size=30, colour="white", transparency=None, font=None, center=None, return_info=False):
        if font == None:
            font = self.font
        colour = get_colour(colour)
        if not str(size) in self.fonts[font]:
            if font in pygame.font.get_fonts():
                self.fonts[font][str(size)] = pygame.font.SysFont(font, size)
            else:
                self.fonts[font][str(size)] = pygame.font.Font(self.font_paths[font], size)
        text = self.fonts[font][str(size)].render(str(text), True, colour)
        x, y = pos
        if center != None:
            if center[3] != 0:
                y = center[1] + center[3]/2 - text.get_height()/2
            if center[2] != 0:
                x = center[0] + center[2]/2 - text.get_width()/2
        if transparency != None:
            text.set_alpha(transparency)
        self.surface.blit(text, (x, y))
        if return_info:
            return (x, y, text.get_width(), text.get_height())
        
    def cut_spritesheet(self, image, rows, columns, amount):
        list = []
        number = 0
        sheet = self.images[image]
        w = sheet.get_width()/columns
        h = sheet.get_height()/rows
        for i in range(rows):
            for j in range(columns):
                number += 1
                list.append(sheet.subsurface(j * w, i * h, w, h))
                if number == amount:
                    return list