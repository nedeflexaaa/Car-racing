import pytest
import pygame
from unittest.mock import MagicMock
import os

# Вимикаємо зображення та звук для Pygame, щоб при тестуванні не вилітали вікна
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"
pygame.init()
pygame.display.set_mode((1, 1))

from Scenes.menu import MenuScene


# --- ФІКСТУРА ---
@pytest.fixture
def menu_scene():
    # Екран потрібен тільки для ініціалізації класу, малювати ніяких зображень не треба
    mock_screen = MagicMock()
    return MenuScene(mock_screen)


# --- ТЕСТ 1: Перевірка стартового стану ---
def test_menu_initial_selection(menu_scene):
    # Перевіряємо, що при запуску меню завжди вибрана перша кнопка (індекс 0)
    assert menu_scene.selected == 0


# --- ТЕСТ 2: Перевірка навігації (Параметризація) ---
@pytest.mark.parametrize("key_pressed, expected_selection", [
    (pygame.K_DOWN, 1),  # Натиснули вниз -> обралась друга кнопка (індекс 1)
    (pygame.K_UP, 2),  # Натиснули вгору (від 0) -> перейшло на останню кнопку (індекс 2)
])
def test_menu_navigation(menu_scene, key_pressed, expected_selection):
    # Створення фейкової події "натискання клавіші"
    event = pygame.event.Event(pygame.KEYDOWN, key=key_pressed)

    # Відправляємо її в метод обробки подій
    menu_scene.handle_event(event)

    # Перевірка, чи змінився індекс вибраної кнопки
    assert menu_scene.selected == expected_selection


# --- ТЕСТ 3: Перевірка вибору ---
def test_menu_return_start(menu_scene):
    # Фіксуємо вибір на кнопці "Start Game" (індекс 0)
    menu_scene.selected = 0

    # Створюємо фейкове натискання Enter
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
    result = menu_scene.handle_event(event)

    # Метод мав повернути рядок "start" для перемикання сцени в main.py
    assert result == "start"
