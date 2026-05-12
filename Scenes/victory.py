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

        if not self.images:
            fallback = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            fallback.fill((0, 150, 0))
            self.images.append(fallback)
        self.current_image_index = 0
        self.last_image_change_time = pygame.time.get_ticks()
        self.image_display_time = 2000

        try:
            pygame.mixer.music.load("Assets/victory/music.mp3")
            pygame.mixer.music.set_volume(0.8)
            pygame.mixer.music.play(-1)  # Грає по колу
        except Exception as e:
            print(f"Помилка музики перемоги: {e}")

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                pygame.mixer.music.stop()
                return "menu"
        return None

    def run(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_image_change_time > self.image_display_time:
            self.current_image_index = (self.current_image_index + 1) % len(self.images)
            self.last_image_change_time = current_time

        current_image = self.images[self.current_image_index]
        self.screen.blit(current_image, (0, 0))

        text = self.font.render("Ви переможець - вітаємо!!! Press ENTER to return to Menu", True, (255, 255, 255))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))

        pygame.draw.rect(self.screen, (0, 0, 0), text_rect.inflate(20, 10))
        self.screen.blit(text, text_rect)
