import pygame
from settings import *

class MenuScene:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 70)
        self.options = ["Start Game", "Car Choice", "Exit"]
        self.selected = 0
        # Завантаження фону
        try:
            self.bg_image = pygame.image.load("Assets/menu/menu_bg.png").convert()
            self.bg_image = pygame.transform.scale(self.bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except Exception:
            self.bg_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.bg_image.fill((20, 20, 20))

        self.button_images = []
        button_files = ["Assets/menu/play_button.png", "Assets/menu/car_choice_button.png", "Assets/menu/exit_button.png"]
        for file_path in button_files:
            try:
                img = pygame.image.load(file_path).convert_alpha()
                img = pygame.transform.scale(img, (300, 80))
                self.button_images.append(img)
            except Exception:
                p = pygame.Surface((300, 80))
                p.fill((100, 100, 100))
                self.button_images.append(p)