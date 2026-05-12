import pytest
import pygame
from unittest.mock import patch
import os
from collections import defaultdict

# Вимикаємо зображення та звук для Pygame, щоб при тестуванні не вилітали вікна
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"
pygame.init()
pygame.display.set_mode((1, 1))

from Entities.car import Car


# --- 1. ФІКСТУРА (Fixture) ---
@pytest.fixture
def test_car():
    return Car(x=100, y=100, car_index=1, color_index=0)


# --- 2. МАРКЕРИ (Test Markers) ---
@pytest.mark.physics
def test_initial_position(test_car):
    assert test_car.position.x == 100
    assert test_car.position.y == 100


# --- 3. МОКУВАННЯ (Mocking) ---
@patch('pygame.key.get_pressed')
@pytest.mark.physics
def test_car_acceleration(mock_keys, test_car):
    # Розумний словник: за замовчуванням всі кнопки False
    fake_keys = defaultdict(bool)
    # Імітація натискання стрілочки ВГОРУ
    fake_keys[pygame.K_UP] = True
    mock_keys.return_value = fake_keys

    # Виклик методу отримання інпуту
    test_car.get_input()

    # Перевіряємо: швидкість мала стати більшою за 0 (дорівнювати прискоренню)
    assert test_car.velocity == test_car.acceleration


# --- 4. ПАРАМЕТРИЗАЦІЯ (Parametrization) ---
@pytest.mark.parametrize("key_pressed, direction", [
    (pygame.K_LEFT, 1),
    (pygame.K_RIGHT, -1)
])
@patch('pygame.key.get_pressed')
@pytest.mark.physics
def test_car_rotation(mock_keys, test_car, key_pressed, direction):
    # Надаємо машині швидкість, бо поворот працює тільки вона їде
    test_car.velocity = 5

    # Використовуємо той самий розумний словник
    fake_keys = defaultdict(bool)
    fake_keys[key_pressed] = True
    mock_keys.return_value = fake_keys

    initial_angle = test_car.angle
    test_car.get_input()

    # Очікуваний кут = старий кут + (швидкість повороту * напрямок)
    expected_angle = initial_angle + (test_car.rotation_speed * direction)
    assert test_car.angle == expected_angle
