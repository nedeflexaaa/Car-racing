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
        self.last_tick = pygame.time.get_ticks()  # Знадобиться пізніше для того аби впевнитись, що просадка фпс
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
        self.player.angle = config["start_angle"]  # Даємо початковий кут
        self.player.rotate()  # Використовуємо метод rotate() з car.py

        self.all_sprites = pygame.sprite.Group()  # Групування спрайтів(поки одного) для можливості в майбутньому
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

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and not self.game_over:
                self.paused = not self.paused
            if event.key == pygame.K_r:
                self.load_map()
            elif event.key == pygame.K_q:
                if getattr(self, 'engine_sound', None):
                    self.engine_sound.stop()
                if getattr(self, 'rev_sound', None):
                    self.rev_sound.stop()
                pygame.mixer.music.stop()
                return "menu"

            if self.game_over:
                if event.key == pygame.K_r:
                    self.load_map()
                elif event.key == pygame.K_q:
                    if getattr(self, 'engine_sound', None):
                        self.engine_sound.stop()
                    if getattr(self, 'rev_sound', None):
                        self.rev_sound.stop()
                    pygame.mixer.music.stop()
                    return "menu"
        return None

    def run(self):
        current_tick = pygame.time.get_ticks()

        # --- ВІДЛІК ПЕРЕД СТАРТОМ ---
        if self.countdown_active:
            elapsed_cd = (current_tick - self.countdown_start) / 1000.0  # Змінюється раз на секунду
            current_step = 3 - int(elapsed_cd)

            if current_step != self.last_countdown_step:  # last_countdown_step на самому початку стоїть 4
                if current_step > 0:
                    if getattr(self, 'beep_sound', None):
                        self.beep_sound.play()  # На випадок, якщо звуку немає прописується getattr
                    # Оскільки якщо немає файлу звуку і викликати команду self.beep_sound.play(), то буде помилка
                elif current_step == 0:
                    if getattr(self, 'go_sound', None):
                        self.go_sound.play()
                self.last_countdown_step = current_step  # Оскільки тут оновлюється пам'ять поки не перепишеться таймером,
                # То пищащий звук буде звучати лише раз на секунду

            if current_step < 0:
                self.countdown_active = False
                self.last_tick = current_tick
                pygame.mixer.music.unpause()
            else:
                self.screen.fill(BG_COLOR)
                self.screen.blit(self.track.image, self.camera.apply(self.track))  # screen.blit - по факту це малювання підготованих картинок
                for sprite in self.all_sprites:
                    self.screen.blit(sprite.image, self.camera.apply(sprite))  # Ставимо спрайт

                text_str = str(current_step) if current_step > 0 else "GO!"
                color = (255, 200, 0) if current_step > 0 else (0, 255, 0)
                text = self.big_font.render(text_str, True, color)

                text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                self.screen.blit(text, text_rect)

                self.last_tick = current_tick
                return None

        dt = (current_tick - self.last_tick) / 1000.0  # Тут не можна просто віднімати по 0.016 кожного кадру (бо 60 FPS це 16 мілісекунд на кадр)
        # бо на слабкому комп'ютері де гра тягне лише 30 фпс буде в два рази більше часу
        self.last_tick = current_tick
        # Тому ми робимо так: записуємо час: self.last_tick = pygame.time.get_ticks() (Наприклад, 1000).
        # Робимо  розрахунки, малюємо кадр. В наступному кадрі дивимося поточний час: current_tick = pygame.time.get_ticks() (Наприклад, 1016).
        # Рахуємо різницю: dt = (1016 - 1000) / 1000 = 0.016 секунди.
        # Віднімаємо цей dt від таймера.І оновлюємо self.last_tick = current_tick, щоб наступного кадру рахувати різницю вже від 1016.

        if self.game_over:
            self.screen.fill((0, 0, 0))
            text = self.big_font.render("TIME'S UP!", True, (255, 0, 0))
            sub_text = self.font.render("Press R to Restart or Q for Menu", True, (255, 255, 255))
            self.screen.blit(text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))
            self.screen.blit(sub_text, (SCREEN_WIDTH // 2 - 220, SCREEN_HEIGHT // 2 + 30))
            return None

        if self.paused:
            pause_text = self.big_font.render("PAUSED (ESC)", True, (255, 255, 255))
            self.screen.blit(pause_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2))
            return None

        self.time_left -= dt
        if self.time_left <= 0:
            self.time_left = 0
            self.game_over = True

        # --- ЗВУК ДВИГУНА ---
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if getattr(self, 'rev_sound', None) and (current_tick - self.last_rev_time > self.rev_cooldown):
                self.rev_sound.play()
                self.last_rev_time = current_tick  # Запис останнього рева двигуна, щоб не спамило звуком

        # --- ФІЗИКА ---
        old_position = pygame.math.Vector2(self.player.position)
        old_angle = self.player.angle

        self.all_sprites.update()
        self.camera.update(self.player)  # Камера слідкує лише за гравцем

        if getattr(self, 'engine_sound', None):
            speed_ratio = abs(self.player.velocity) / self.player.max_speed  # Чим більша швидкість, тим гучніше двигун
            new_volume = 0.2 + (0.8 * speed_ratio)
            self.engine_sound.set_volume(new_volume)

        # Зіткнення з трасою
        if pygame.sprite.collide_mask(self.player, self.track):
            if getattr(self, 'crash_sound', None) and abs(self.player.velocity) > 2:  # Звук лише при такій швидкості
                self.crash_sound.play()

            self.player.position = old_position
            self.player.angle = old_angle
            self.player.rect.center = self.player.position
            self.player.rotate()
            self.player.velocity = -(self.player.velocity * 0.5)
            # По факту при зіткненні повертаємо машинку на позицію, де вона була кадр тому і даємо вдвічі меншу швидкість
            # У протилежному напрямку

        # Чекпоінти
        if self.player.rect.colliderect(self.checkpoints[self.current_checkpoint]):
            self.current_checkpoint += 1

            if self.current_checkpoint >= len(self.checkpoints):
                self.current_checkpoint = 0
                self.lap += 1

                if self.lap > self.target_laps:
                    self.current_map_index += 1

                    if self.current_map_index >= len(self.maps_config):
                        if getattr(self, 'engine_sound', None):
                            self.engine_sound.stop()
                        if getattr(self, 'rev_sound', None):
                            self.rev_sound.stop()
                        pygame.mixer.music.stop()
                        return "victory"

                    self.load_map()
                    return None

        # --- МАЛЮВАННЯ ---
        self.screen.fill(BG_COLOR)
        self.screen.blit(self.track.image, self.camera.apply(self.track))

        for i, cp in enumerate(self.checkpoints):
            adjusted_rect = self.camera.apply_rect(cp)
            color = (0, 255, 0) if i == self.current_checkpoint else (255, 0, 0)
            pygame.draw.rect(self.screen, color, adjusted_rect, 3)
            debug_text = self.font.render(f"CP {i}", True, color)
            self.screen.blit(debug_text, (adjusted_rect.x, adjusted_rect.y - 35))

        for sprite in self.all_sprites:  # Малюємо всі спрайти зі зсувом камери
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        # Наприклад екран має ширину 1000 пікселів (центр = 500). машина стоїть на карті на координаті X = 8000.
        # Поруч із машиною стоїть чекпоінт на координаті X = 8200. Камера рахує зміщення через свій (update)
        # Зсув камери = -7500. Беремо реальні координати машинки (8000) і додаємо зсув (-7500) => 500 нова координата машинки
        # Точно такий самий зсув і до всіх інших об'єктів

        # --- HUD ---
        lap_text = self.font.render(f"Lap: {self.lap}/{self.target_laps}", True, (255, 255, 255))
        map_text = self.font.render(f"Map: {self.current_map_index + 1}/{len(self.maps_config)}", True, (255, 255, 255))

        timer_color = (255, 0, 0) if self.time_left <= 10 else (255, 255, 255)
        timer_text = self.font.render(f"Time: {int(self.time_left)}", True, timer_color)

        self.screen.blit(lap_text, (20, 20))
        self.screen.blit(map_text, (20, 60))
        self.screen.blit(timer_text, (SCREEN_WIDTH - 150, 20))
        # Малювання різних надписів

        return None
