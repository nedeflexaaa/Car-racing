import pygame
from settings import *


class Car(pygame.sprite.Sprite): #Car є нащадком базового класу Sprite, який написали розробники PyGame.
    # Змінну self передано на випадок створення декількох машин
    # А також для звернення до конкретно створеної машини
    def __init__(self, x, y, car_index=0, color_index=0, car_size=(20, 40)):
        super().__init__() # Базовий клас Sprite вже має свій власний, прихований метод __init__()
        # Якщо видалити super().__init__(), то init, який був наслідуваний від Sprite буде проігнорований
        # Щоб цього не слалось, використовується super().__init__()

        # --- 1. НАЛАШТУВАННЯ ФІЗИКИ ДЛЯ РІЗНИХ АВТО ---
        if car_index == 0:  # Fast & Slippery
            self.max_speed = MAX_SPEED + 2
            self.acceleration = ACCELERATION
            self.rotation_speed = ROTATION_SPEED - 1
            self.friction = FRICTION - 0.02
        elif car_index == 1:  # Balanced Car
            self.max_speed = MAX_SPEED
            self.acceleration = ACCELERATION + 0.05
            self.rotation_speed = ROTATION_SPEED + 1
            self.friction = FRICTION
        else:  # Slow & Heavy
            self.max_speed = MAX_SPEED - 2
            self.acceleration = ACCELERATION + 0.1
            self.rotation_speed = ROTATION_SPEED + 2
            self.friction = FRICTION + 0.05
