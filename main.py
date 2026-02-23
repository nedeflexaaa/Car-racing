# main.py
import pygame
import sys
from settings import *
from Scenes.game import GameScene

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Car Racing")
clock = pygame.time.Clock()

game_scene = GameScene(screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    game_scene.run()

    pygame.display.flip()
    clock.tick(FPS)