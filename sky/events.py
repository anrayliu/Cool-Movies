import pygame


class Events:
    def __init__(self):
        self.update()
        
    def update(self):
        self.quit = False
        self.left_click = False
        self.right_click = False
        self.input_name = None
        self.input_key = None
        self.wheel = 0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.left_click = True
                elif event.button == 3:
                    self.right_click = True
            elif event.type == pygame.KEYDOWN:
                self.input_name = pygame.key.name(event.key)
                self.input_key = event.unicode
            elif event.type == pygame.MOUSEWHEEL:
                self.wheel = event.y
                
        self.keys_held = pygame.key.get_pressed()
        self.mouse_held = pygame.mouse.get_pressed()
        self.mouse = self.x, self.y = pygame.mouse.get_pos()