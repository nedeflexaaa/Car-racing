import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT


class Camera:
    def __init__(self, map_width, map_height):
        # map_width та map_height - розміри всієї картинки траси
        self.camera = pygame.Rect(0, 0, map_width, map_height)
        self.width = map_width
        self.height = map_height

    def update(self, target):
        # 1. Рахуємо ідеальний центр, ніби обмежень немає
        x = -target.rect.centerx + int(SCREEN_WIDTH / 2)
        y = -target.rect.centery + int(SCREEN_HEIGHT / 2)

    def apply(self, entity):
        # Повертає нові координати об'єкта з урахуванням зсуву камери
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        # Те саме, але для звичайних прямокутників
        return rect.move(self.camera.topleft)