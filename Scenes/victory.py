import pygame
from settings import *


class VictoryScene:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 50)

        self.images = []
        image_paths = [
            "Assets/victory/like.jpg",
            "Assets/victory/yalta.jpg",
            "Assets/victory/homer.jpg",
            "Assets/victory/breaking_bad.jpg"
        ]
for path in image_paths:
            try:
                img = pygame.image.load(path).convert()
                img = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
                self.images.append(img)
            except Exception as e:
                print(f"Помилка завантаження картинки {path}: {e}")
                
        # Якщо жодна картинка не завантажилась, робимо зелену заглушку
        if not self.images:
            fallback = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            fallback.fill((0, 150, 0))
            self.images.append(fallback)