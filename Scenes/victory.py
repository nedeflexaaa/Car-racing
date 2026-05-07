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
