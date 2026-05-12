import pygame
from settings import *


class CarSelectScene:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 60)
        self.title_font = pygame.font.SysFont(None, 80)

        # Маленький шрифт для підказки про кольори
        self.hint_font = pygame.font.SysFont(None, 40)

        self.options = ["Fast & Slippery", "Balanced Car", "Slow & Heavy", "Back to Menu"]
        self.selected = 0

        # Масив, що запам'ятовує обраний колір (від 0 до 3) для кожної з 3 машин
        self.selected_colors = [0, 0, 0]

        # --- ЗАВАНТАЖЕННЯ КАРТИНОК МАШИН (3 типи авто по 4 кольори) ---
        self.car_images = []

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

        # Базові кольори для заглушок (якщо файлу немає)
        debug_colors = [(255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 255, 0)]

        for car_type_paths in image_paths:  # Цикл з додавання зображень з різним кольором кожній машинці
            color_variants = []  # Пустий масив
            for color_index, path in enumerate(car_type_paths):  # Проходження по масиву: кожний колір дає всій path там має свій color_index
                try:
                    img = pygame.image.load(path).convert_alpha()
                    img = pygame.transform.scale(img, (120, 240))
                    color_variants.append(img)  # Саме додавання зображення в масив
                except FileNotFoundError:
                    # Якщо картинки немає, робимо заглушку відповідного кольору
                    placeholder = pygame.Surface((120, 240))
                    placeholder.fill(debug_colors[color_index])
                    color_variants.append(placeholder)
            self.car_images.append(color_variants)  # Завантаження кожного з маленьких масивчіків в один побільше

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:  # З всіх івентів ми перевіряємо лише ті, де натискаються клавіші.
            # Навігація по списку машин (Вгору/Вниз)
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)

            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)

        # Навігація по кольорах (Вліво/Вправо)
            elif event.key == pygame.K_LEFT:
                if self.selected < 3:
                    # Дивимося, скільки кольорів є САМЕ У ЦІЄЇ машини
                    num_colors = len(self.car_images[self.selected])
                    self.selected_colors[self.selected] = (self.selected_colors[self.selected] - 1) % num_colors

            elif event.key == pygame.K_RIGHT:
                if self.selected < 3:
                    num_colors = len(self.car_images[self.selected])
                    self.selected_colors[self.selected] = (self.selected_colors[self.selected] + 1) % num_colors

        # Вибір
            elif event.key == pygame.K_RETURN:
                if self.selected == 3:  # Кнопка "Back to Menu"
                    return "menu"
                else:
                    color_idx = self.selected_colors[self.selected]
                    # Повертаємо ДВА індекси: номер машини і номер кольору
                    return f"car_selected_{self.selected}_{color_idx}"

            elif event.key == pygame.K_ESCAPE:
                return "menu"

        return None

    def run(self):
        self.screen.fill((20, 20, 40))

        title = self.title_font.render("SELECT YOUR CAR", True, (255, 200, 0))
        self.screen.blit(title, (SCREEN_WIDTH // 2 - 250, 100))

        for i, option in enumerate(self.options):
            color = (0, 255, 0) if i == self.selected else (255, 255, 255)
            text = self.font.render(option, True, color)
            self.screen.blit(text, (SCREEN_WIDTH // 2 - 350, 250 + i * 80))

        # --- МАЛЮЄМО МАШИНКУ СПРАВА ---
        if self.selected < 3:
            # Беремо поточний колір для поточної машини
            color_idx = self.selected_colors[self.selected]
            current_image = self.car_images[self.selected][color_idx]

            image_rect = current_image.get_rect(center=(SCREEN_WIDTH // 2 + 200, 340))
            self.screen.blit(current_image, image_rect)

            # Малюємо підказку під машинкою
            hint_text = self.hint_font.render(f"< Color {color_idx + 1} >", True, (150, 150, 150))
            hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2 + 200, 480))
            self.screen.blit(hint_text, hint_rect)
