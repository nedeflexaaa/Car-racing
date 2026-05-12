import pytest
import pygame
from unittest.mock import patch, MagicMock
import os

# Вимикаємо зображення та звук для Pygame, щоб при тестуванні не вилітали вікна
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"
pygame.init()
pygame.display.set_mode((1, 1))

from Scenes.game import GameScene


# --- ФІКСТУРА  ---
@pytest.fixture
@patch('pygame.image.load')
@patch('pygame.mixer.Sound')
@patch('pygame.mixer.music.load')
def game_scene(mock_music, mock_sound, mock_img):
    # 1. Створюємо маленьку картинку заглушку
    dummy_surface = pygame.Surface((100, 100))

    # 2. Кажемо, щоб наш мок повертав цю заглушку, коли викликається .convert_alpha()
    mock_img.return_value.convert_alpha.return_value = dummy_surface
    mock_img.return_value.convert.return_value = dummy_surface

    # 3. Екран теж зробили справжнім, щоб не було конфліктів
    mock_screen = pygame.Surface((1280, 720))

    return GameScene(mock_screen, car_index=0, color_index=0)


# --- ТЕСТ 1: Перевірка системи ПАУЗИ ---
def test_game_pause_toggle(game_scene):
    # На початку гра не на паузі
    assert game_scene.paused == False

    # Створення натискання ESC
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)
    game_scene.handle_event(event)

    # Перевірка, чи спрацювала пауза
    assert game_scene.paused == True

    # Натискаємо ESC ще раз, щоб зняти з паузи
    game_scene.handle_event(event)
    assert game_scene.paused == False


# --- ТЕСТ 2: Перевірка виходу в меню ---
def test_game_map_config_loading(game_scene):
    # Коли завантажуємо першу карту (індекс 0), час має стати 180 (з словника configs)
    assert game_scene.time_left == 180
    assert game_scene.target_laps == 1
    # Машинка мала з'явитися під кутом 90 градусів
    assert game_scene.player.angle == 90


# --- ТЕСТ 3: Перевірка виходу в меню ---
def test_game_quit_to_menu(game_scene):
    # Arrange (Підготовка): Створення події натискання клавіші Q
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_q)

    # Передаємо цю подію в обробник сцени
    result = game_scene.handle_event(event)

    # Переконуємося, що сцена наказала повернутися в меню
    assert result == "menu"
