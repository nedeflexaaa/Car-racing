import pygame
import sys
import math

# --------------- Ініціалізація ----------------
pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Top-Down Racing (Demo)")

clock = pygame.time.Clock()

# --------------- Машинка ----------------
car_pos = pygame.Vector2(WIDTH // 2, HEIGHT // 2)
car_angle = 0          # кут повороту
car_speed = 0

MAX_SPEED = 6
ACCELERATION = 0.2
ROTATION_SPEED = 3
FRICTION = 0.05

# Простий "спрайт" машинки
car_surface = pygame.Surface((40, 20))
car_surface.fill((255, 0, 0))  # червона машинка
car_rect = car_surface.get_rect(center=car_pos)

# --------------- Головний цикл ----------------
while True:
    dt = clock.tick(60) / 1000  # delta time (поки просто ігноруй)

    # --- Події ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    # --- Керування ---
    if keys[pygame.K_w]:
        car_speed += ACCELERATION
    if keys[pygame.K_s]:
        car_speed -= ACCELERATION

    if keys[pygame.K_a]:
        car_angle += ROTATION_SPEED
    if keys[pygame.K_d]:
        car_angle -= ROTATION_SPEED

    # Обмеження швидкості
    car_speed = max(-MAX_SPEED, min(MAX_SPEED, car_speed))

    # Тертя
    if car_speed > 0:
        car_speed -= FRICTION
    elif car_speed < 0:
        car_speed += FRICTION

    # --- Рух машинки ---
    radians = math.radians(car_angle)
    car_pos.x += math.cos(radians) * car_speed
    car_pos.y -= math.sin(radians) * car_speed

    car_rect.center = car_pos

    # --- Малювання ---
    screen.fill((30, 30, 30))  # фон

    rotated_car = pygame.transform.rotate(car_surface, car_angle)
    rotated_rect = rotated_car.get_rect(center=car_rect.center)
    screen.blit(rotated_car, rotated_rect)

    pygame.display.flip()
