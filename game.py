import pygame
from settings import *
from Entities.car import Car
from Entities.map import TrackMap
from Utils.camera import Camera

class GameScene:
    def __init__(self, screen, car_index=0, color_index=0):
        self.screen = screen
        self.car_index = car_index
        self.color_index = color_index
        self.paused = False
        self.game_over = False

        # --- СИСТЕМА УНІКАЛЬНИХ РІВНІВ ---
        # Цей патерн знизу - Dictionary Configs. Він заміняє тону if\else, але тепер коли наприклад гравець переходить
        # на наступний рівень, робиш: config = self.maps_config[self.current_map_index].
        # Тепер config — це словник з даними саме поточної карти.
        self.maps_config = [
            {  # --- КАРТА 1 ---
                "visual": "Assets/maps/Map_1/map1.png",
                "hitbox": "Assets/maps/Map_1/map1_hitbox.png",
                "map_class": TrackMap,
                "start_pos": (3560, 2680),
                "start_angle": 90,
                "time_limit": 180,
                "target_laps": 1,
                "car_size": (15, 30),
                "checkpoints": [
                    pygame.Rect(3100, 2630, 26, 80),
                    pygame.Rect(844, 200, 66, 160),
                    pygame.Rect(6020, 2140, 26, 60),
                    pygame.Rect(3740, 2630, 26, 80),
                ]
            },
            {  # --- КАРТА 2 ---
                "visual": "Assets/maps/Map_2/map2.png",
                "hitbox": "Assets/maps/Map_2/map2_hitbox.png",
                "map_class": TrackMap,
                "start_pos": (3620, 2700),
                "start_angle": 90,
                "time_limit": 180,
                "target_laps": 1,
                "car_size": (15, 30),
                "checkpoints": [
                    pygame.Rect(3580, 2680, 26, 80),
                    pygame.Rect(1210, 320, 66, 160),
                    pygame.Rect(4450, 180, 30, 60),
                    pygame.Rect(3830, 2680, 26, 80)
                ]
            },
            {  # --- КАРТА 3 ---
                "visual": "Assets/maps/Map_3/map3.png",
                "hitbox": "Assets/maps/Map_3/map3_hitbox.png",
                "map_class": TrackMap,
                "start_pos": (6000, 990),
                "start_angle": 0,
                "time_limit": 180,
                "target_laps": 1,
                "car_size": (15, 30),
                "checkpoints": [
                    pygame.Rect(5930, 1000, 120, 20),
                    pygame.Rect(4350, 1090, 66, 80),
                    pygame.Rect(155, 1820, 96, 70),
                    pygame.Rect(5960, 1130, 120, 20)
                ]
            },
        ]

        self.current_map_index = 0
        self.font = pygame.font.SysFont(None, 40)
        self.big_font = pygame.font.SysFont(None, 80)
        self.last_tick = pygame.time.get_ticks() # Знадобиться пізніше для того аби впевнитись, що просадка фпс
        # не впливала на роботу таймера
