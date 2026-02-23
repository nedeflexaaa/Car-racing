# Utils/camera.py
import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT


class Camera:
    def __init__(self, map_width, map_height):
        # map_width та map_height - це розміри всієї картинки траси
        self.camera = pygame.Rect(0, 0, map_width, map_height)
        self.width = map_width
        self.height = map_height

    def apply(self, entity):
        # Цей метод бере об'єкт (наприклад, машинку або перешкоду)
        # і повертає його нові координати з урахуванням зсуву камери
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        # Те саме, але для звичайних прямокутників (наприклад, для малювання фону)
        return rect.move(self.camera.topleft)

    def update(self, target):
        # target - це наша машинка. Ми вираховуємо зсув так, щоб вона була по центру
        x = -target.rect.centerx + int(SCREEN_WIDTH / 2)
        y = -target.rect.centery + int(SCREEN_HEIGHT / 2)

        # (Опціонально) Тут можна додати обмеження, щоб камера не виходила за межі карти,
        # але для гонок часто прикольно, коли камера може трохи "вилітати" за край.

        self.camera = pygame.Rect(x, y, self.width, self.height)