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

# --- ЗАВАНТАЖЕННЯ ЗВУКІВ ---
        try:
            pygame.mixer.music.load("Assets/sounds/meat.mp3")
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play(-1)
        except Exception:
            print("Музику не знайдено")

        try:
            self.crash_sound = pygame.mixer.Sound("Assets/sounds/crash.mp3")
            self.crash_sound.set_volume(0.7)
        except Exception:
            self.crash_sound = None

        try:
            self.engine_sound = pygame.mixer.Sound("Assets/sounds/engine_idle.wav")
            self.engine_sound.set_volume(1.5)
            self.engine_sound.play(-1)

            self.rev_sound = pygame.mixer.Sound("Assets/sounds/engine_rev.mp3")
            self.rev_sound.set_volume(1.5)
        except Exception:
            self.engine_sound = None
            self.rev_sound = None

        self.last_rev_time = 0
        self.rev_cooldown = 2500

        try:
            self.beep_sound = pygame.mixer.Sound("Assets/sounds/beep.mp3")
            self.beep_sound.set_volume(0.8)
            self.go_sound = pygame.mixer.Sound("Assets/sounds/go.mp3")
            self.go_sound.set_volume(0.8)
        except Exception:
            self.beep_sound = None
            self.go_sound = None

        self.load_map()



    def load_map(self):
        config = self.maps_config[self.current_map_index]
        MapClass = config["map_class"]
        self.track = MapClass(config["visual"], config["hitbox"])

        start_x, start_y = config["start_pos"]
        self.player = Car(start_x, start_y, self.car_index, self.color_index, config["car_size"])
        self.player.angle = config["start_angle"] # Даємо початковий кут
        self.player.rotate() # Використовуємо метод rotate() з car.py

        self.all_sprites = pygame.sprite.Group() # Групування спрайтів(поки одного) для можливості в майбутньому
        # додати інші машини\перешкоди
        self.all_sprites.add(self.player)

        self.camera = Camera(self.track.rect.width, self.track.rect.height)
        self.camera.update(self.player)

        self.checkpoints = config["checkpoints"]
        self.time_left = config["time_limit"]
        self.target_laps = config["target_laps"]

        self.current_checkpoint = 0
        self.lap = 1
        self.last_tick = pygame.time.get_ticks()
        self.game_over = False
        self.paused = False

        self.countdown_active = True
        self.countdown_start = pygame.time.get_ticks()
        self.last_countdown_step = 4

        pygame.mixer.music.pause()
        self.last_tick = pygame.time.get_ticks()