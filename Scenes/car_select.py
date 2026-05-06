import pygame
from settings import *

class CarSelectScene:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 60)
        self.title_font = pygame.font.SysFont(None, 80)
        self.hint_font = pygame.font.SysFont(None, 40)
        self.options = ["Fast & Slippery", "Balanced Car", "Slow & Heavy", "Back to Menu"]
        self.selected = 0
        self.selected_colors = [0, 0, 0]

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

        for car_type_paths in image_paths: # Цикл з додавання зображень з різним кольором кожній машинці
            color_variants = []  # Пустий масив
            for color_index, path in enumerate(car_type_paths): # Проходження по масиву: кожний колір дає всій path там має свій color_index
                try:
                    img = pygame.image.load(path).convert_alpha()
                    img = pygame.transform.scale(img, (120, 240))
                    color_variants.append(img) # Саме додавання зображення в масив
                except FileNotFoundError:
                    # Якщо картинки немає, робимо заглушку відповідного кольору
                    placeholder = pygame.Surface((120, 240))
                    placeholder.fill(debug_colors[color_index])
                    color_variants.append(placeholder)
            self.car_images.append(color_variants)
                   
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
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
        return None