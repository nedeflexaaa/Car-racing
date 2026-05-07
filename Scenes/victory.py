import pygame
from settings import *


class VictoryScene:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 50)

        self.images = []
        image_paths = [
            "Assets/victory/like.jpg",
            "Assets/victory/yalta.jpg",
            "Assets/victory/homer.jpg",
            "Assets/victory/breaking_bad.jpg"
        ]
        for path in image_paths:
            try:
                img = pygame.image.load(path).convert()
                img = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
                self.images.append(img)
            except Exception as e:
                print(f"Помилка завантаження картинки {path}: {e}")
                
        # Якщо жодна картинка не завантажилась, робимо зелену заглушку
        if not self.images:
            fallback = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            fallback.fill((0, 150, 0))
            self.images.append(fallback)
                # --- НАЛАШТУВАННЯ СЛАЙДШОУ ---
        self.current_image_index = 0
        self.last_image_change_time = pygame.time.get_ticks()
        self.image_display_time = 2000  # Скільки мілісекунд показувати 1 картинку

        # --- ЗАВАНТАЖЕННЯ МУЗИКИ ---
        try:
            pygame.mixer.music.load("Assets/victory/music.mp3")
            pygame.mixer.music.set_volume(0.8)
            pygame.mixer.music.play(-1)  # Грає по колу
        except Exception as e:
            print(f"Помилка музики перемоги: {e}")
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            # Якщо натиснути Enter або Esc - виходимо в меню
            if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                pygame.mixer.music.stop()  # Вимикаємо фанфари
                return "menu"
        return None