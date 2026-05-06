import pygame
from settings import *

class CarSelectScene:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 60)
        self.title_font = pygame.font.SysFont(None, 80)
        self.hint_font = pygame.font.SysFont(None, 40)
        self.options = ["Fast & Slippery", "Balanced Car", "Slow & Heavy", "Back to Menu"]
        self.selected = 0
        self.selected_colors = [0, 0, 0]
        