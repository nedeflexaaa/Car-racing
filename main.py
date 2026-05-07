import pygame
import sys
from settings import *
from Scenes.menu import MenuScene
from Scenes.game import GameScene
from Scenes.car_select import CarSelectScene
from Scenes.victory import VictoryScene

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Car Racing")
clock = pygame.time.Clock()

current_scene = "menu"

# Ініціалізація сцен(створення об'єктів з відповідних класів)
menu_scene = MenuScene(screen)
car_select_scene = CarSelectScene(screen)
game_scene = None
victory_scene = None

chosen_car_index = 0
chosen_color_index = 0