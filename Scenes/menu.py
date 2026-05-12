import pygame
from settings import *


class MenuScene:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 70)
        self.options = ["Start Game", "Car Choice", "Exit"]
        self.selected = 0

        # --- ЗАВАНТАЖЕННЯ ЗОБРАЖЕНЬ ---
        # 1. Задній фон
        try:
            self.bg_image = pygame.image.load("Assets/menu/menu_bg.png").convert()
            self.bg_image = pygame.transform.scale(self.bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except Exception:
            self.bg_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.bg_image.fill((20, 20, 20))

        # 2. Кнопки меню
        self.button_images = []
        button_files = [
            "Assets/menu/play_button.png",
            "Assets/menu/car_choice_button.png",
            "Assets/menu/exit_button.png"
        ]

        for file_path in button_files:
            try:
                img = pygame.image.load(file_path).convert_alpha()
                # Всі кнопки однакового розміру
                img = pygame.transform.scale(img, (300, 80))
                self.button_images.append(img)
            except Exception:
                p = pygame.Surface((300, 80))
                p.fill((100, 100, 100))
                self.button_images.append(p)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)  # Остача від ділення(%) треба для того, аби
                # При натисканні вниз на останній кнопці вибір переходив на гору списку

            if event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)  # Аналогічно

            if event.key == pygame.K_RETURN:
                if self.selected == 0:
                    return "start"
                elif self.selected == 1:
                    return "choice"
                elif self.selected == 2:
                    return "exit"

        return None

    def run(self):
        # МАЛЮЄМО ФОН
        self.screen.blit(self.bg_image, (0, 0))

        for i, option in enumerate(self.options):
            # Задаємо координати списку кнопок
            x_pos = SCREEN_WIDTH - 350
            y_pos = 300 + i * 100

            # Беремо картинку з нашого списку під потрібним індексом
            current_btn_image = self.button_images[i]

            image_rect = current_btn_image.get_rect(topleft=(x_pos, y_pos))

            # Якщо кнопка вибрана, малюємо навколо неї червону рамку
            if self.selected == i:
                pygame.draw.rect(self.screen, (255, 0, 0), image_rect.inflate(10, 10), 4)

            # Малюємо саму кнопку
            self.screen.blit(current_btn_image, image_rect)
