import pygame


class TrackMap(pygame.sprite.Sprite):
    def __init__(self, visual_path, hitbox_path):
        super().__init__()  # Базовий клас Sprite вже має свій власний, прихований метод __init__()
        # Якщо видалити super().__init__(), то init, який був наслідуваний від Sprite буде проігнорований
        # Щоб цього не слалось, використовується super().__init__()

        # 1. Завантажуємо оригінальні картинки
        original_image = pygame.image.load(visual_path).convert_alpha()
        original_hitbox = pygame.image.load(hitbox_path).convert_alpha()

        # --- ЗБІЛЬШЕННЯ КАРТИ ---
        # Варіант А: Вказати точні розміри в пікселях (наприклад, 2000 на 2000)
        # new_size = (2000, 2000)

        # Варіант Б: Збільшити пропорційно у 2 рази (цей оформлено)
        new_width = original_image.get_width() * 2
        new_height = original_image.get_height() * 2
        new_size = (new_width, new_height)

        # Застосовуємо масштаб до обох картинок
        self.image = pygame.transform.scale(original_image, new_size)
        hitbox_image = pygame.transform.scale(original_hitbox, new_size)
        # ------------------------

        # 2. Отримуємо координати вже з нової, збільшеної картинки
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)

        # 3. Створюємо маску зі ЗБІЛЬШЕНОГО хітбоксу
        self.mask = pygame.mask.from_surface(hitbox_image)
