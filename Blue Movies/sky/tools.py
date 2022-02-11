from sky.colours import *
import sys #exit
import os #path.exists, path.join
import ctypes #messagebox
import pygame 


def get_colour(value):
    try:
        colour = globals()[value.upper().replace(" ", "_")]
    except AttributeError:
        colour = value
    return colour
    
    
def close():
    pygame.quit()
    sys.exit()
    
    
def confirm_assets(list):
    errors = []
    for path in list:
        if not os.path.exists(path):
            errors.append(path)
    text = ""
    for error in errors:
        text += error + "\n"
    if text != "":
        ctypes.windll.user32.MessageBoxW(0, "Please reinstall; the following paths were not found:\n" + text, "Error", 0)
        close()
        
def draw_round_rect(surface, colour, rect, r):
    x, y, w, h = rect
    colour = get_colour(colour)

    pygame.draw.ellipse(surface, colour,(x,y,r,r))
    pygame.draw.ellipse(surface, colour,(x+w-r,y,r,r))
    pygame.draw.ellipse(surface, colour,(x,y+h-r,r,r))
    pygame.draw.ellipse(surface, colour,(x+w-r,y+h-r,r,r))

    pygame.draw.rect(surface, colour,(x+r/2,y,w-r,r))
    pygame.draw.rect(surface, colour,(x+r/2,y+h-r/2-r/2,w-r,r))
    pygame.draw.rect(surface, colour,(x,y+r/2,r,h-r))
    pygame.draw.rect(surface, colour,(x+w-r,y+r/2,r,h-r))

    pygame.draw.rect(surface, colour,(x+r/2,y+r/2,w-r,h-r))