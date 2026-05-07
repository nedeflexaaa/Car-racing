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

        # --- 2. ШЛЯХИ ДО ВСІХ ВАРІАНТІВ МАШИН ТА КОЛЬОРІВ ---
        image_paths = [
            [  # Машина 1 (Fast & Slippery)
                "Assets/cars/Car_1/blue.png",
                "Assets/cars/Car_1/pink.png",
                "Assets/cars/Car_1/purple.png",
                "Assets/cars/Car_1/red.png"
            ],
            [  # Машина 2 (Balanced)
                "Assets/cars/Car_2/blue.png",
                "Assets/cars/Car_2/pink.png",
                "Assets/cars/Car_2/purple.png",
                "Assets/cars/Car_2/red.png"
            ],
            [  # Машина 3 (Slow & Heavy)
                "Assets/cars/Car_3/purple(special).png",
                "Assets/cars/Car_3/red(special).png"
            ]
        ]
        # --- 3. ЗАВАНТАЖЕННЯ КАРТИНКИ ---
        try:
            correct_image_path = image_paths[car_index][color_index]  # Беремо шлях машинки з масиву
            self.original_image = pygame.image.load(correct_image_path).convert_alpha()
            # Зміна розмірів машини відносно мапи
            self.original_image = pygame.transform.scale(self.original_image, car_size)
        except Exception:
            self.original_image = pygame.Surface(car_size)  # Затичка на випадок відсутності зображення
            self.original_image.fill((0, 255, 0))
        # --- 4. НАЛАШТУВАННЯ СПРАЙТА ---
        # Якщо перед змінними в __init__ не прописати self., то вони помруть відразу після закінчення методу
        # При додаванні self., ми кріпимо змінну до конкретної машини назавжди

        self.image = self.original_image
        self.rect = self.image.get_rect() # "хітбокс" у формі прямокутника
        # Він зберігає координати машини та її розмір. PyGame використовує rect, щоб розуміти, куди ставити картинку.
        self.rect.center = (x, y) # Для малювання машинки на екрані, приймає лише цілі значення
        self.mask = pygame.mask.from_surface(self.image) # "ідеальний хітбокс". rect - це просто тупий квадрат навколо машини,
        # Це потрібно для точних зіткнень зі стінами, щоб не врізатись порожнім кутком зображення

        self.position = pygame.math.Vector2(x, y)
        self.velocity = 0
        self.angle = 0