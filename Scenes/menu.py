import pygame
from settings import *

class MenuScene:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 70)
        self.options = ["Start Game", "Car Choice", "Exit"]
        self.selected = 0