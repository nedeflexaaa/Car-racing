import pygame
import math
from settings import *


class Car(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # Завантаження картинки
        try:
            self.original_image = pygame.image.load('Assets/cars/car.png').convert_alpha()
            # Масштабуємо, якщо картинка занадто велика
            self.original_image = pygame.transform.scale(self.original_image, (20, 40))
        except FileNotFoundError:
            # Аварійний квадрат, якщо картинки немає
            self.original_image = pygame.Surface((40, 80))
            self.original_image.fill((0, 255, 0))

        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.mask = pygame.mask.from_surface(self.image)

        # Параметри руху
        self.position = pygame.math.Vector2(x, y)
        self.velocity = 0
        self.angle = 0

    def get_input(self):
        keys = pygame.key.get_pressed()

        # Газ / Гальма
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if self.velocity < 0:
                self.velocity += BRAKE_STRENGTH  # Швидше гальмуємо
            else:
                self.velocity += ACCELERATION
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if self.velocity > 0:
                self.velocity -= BRAKE_STRENGTH
            else:
                self.velocity -= ACCELERATION

        # Повороти (працюють тільки якщо машина їде)
        if abs(self.velocity) > 0.1:
            # Інвертуємо керування при задньому ході для реалізму
            direction = 1 if self.velocity > 0 else -1

            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.angle += ROTATION_SPEED * direction
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.angle -= ROTATION_SPEED * direction

    def move(self):
        # Обмеження швидкості
        if self.velocity > MAX_SPEED:
            self.velocity = MAX_SPEED
        if self.velocity < -MAX_SPEED / 2:  # Задній хід повільніший
            self.velocity = -MAX_SPEED / 2

        # Тертя (поступова зупинка)
        if self.velocity > 0:
            self.velocity -= FRICTION
            if self.velocity < 0: self.velocity = 0
        elif self.velocity < 0:
            self.velocity += FRICTION
            if self.velocity > 0: self.velocity = 0

        # Математика руху: переводимо кут і швидкість у координати X та Y
        # -self.angle тому що в pygame кути йдуть проти годинникової стрілки
        rad = math.radians(self.angle)
        self.position.x -= math.sin(rad) * self.velocity
        self.position.y -= math.cos(rad) * self.velocity

        self.rect.center = self.position

    def rotate(self):
        # Обертання картинки навколо центру
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.get_input()
        self.move()
        self.rotate()