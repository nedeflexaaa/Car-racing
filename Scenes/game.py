# Scenes/game.py
import pygame
from settings import *
from Entities.car import Car
from Entities.map import Map
from Utils.camera import Camera


class GameScene:
    def __init__(self, screen):
        self.screen = screen

        # Завантаження карти
        self.track = Map('Assets/maps/track.png', 'Assets/maps/imageedit_1_6866009776.png')


        # Створення машинки
        self.player = Car(1200, 1100)
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

        # Камера бере розміри прямо з картинки карти
        self.camera = Camera(self.track.rect.width, self.track.rect.height)

    def run(self):
        # 1. ЗАПАМ'ЯТОВУЄМО стару позицію до руху
        old_position = pygame.math.Vector2(self.player.position)

        # 2. Оновлюємо машинку
        self.all_sprites.update()
        self.camera.update(self.player)

        # 3. ПЕРЕВІРКА ЗІТКНЕНЬ
        # collide_mask автоматично перевіряє, чи накладаються пікселі масок одна на одну
        if pygame.sprite.collide_mask(self.player, self.track):
            # Якщо врізалися: повертаємо машинку на координати до зіткнення
            self.player.position = old_position
            self.player.rect.center = self.player.position
            # І робимо відскок (зменшуємо швидкість вдвічі і міняємо напрямок)
            self.player.velocity = -(self.player.velocity * 0.5)

        # 4. Малюємо все
        self.screen.fill(BG_COLOR)

        # Спочатку малюємо саму карту (її теж треба зсувати камерою)
        self.screen.blit(self.track.image, self.camera.apply(self.track))

        # Потім малюємо машинку поверх карти
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))