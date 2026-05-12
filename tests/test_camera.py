import pytest
import pygame
from Utils.camera import Camera
from settings import SCREEN_WIDTH, SCREEN_HEIGHT


# Створення фейкового гравця, щоб не імпортувати складний клас Car з багатьма налаштуваннями
class MockPlayer:
    def __init__(self, x, y):
        self.rect = pygame.Rect(0, 0, 20, 40)
        self.rect.center = (x, y)


@pytest.fixture
def test_cam():
    # Створення камери для умовної карти розміром 3000x3000
    return Camera(map_width=3000, map_height=3000)


@pytest.mark.physics
def test_camera_top_left_limits(test_cam):
    # Ставимо гравця далеко за межі карти вліво вгору
    player = MockPlayer(-500, -500)
    test_cam.update(player)

    # Камера має впертися в край карти і не стати додатнім числом
    assert test_cam.camera.x == 0
    assert test_cam.camera.y == 0


@pytest.mark.physics
def test_camera_bottom_right_limits(test_cam):
    # Ставимо гравця далеко за межі карти вправо вниз
    player = MockPlayer(10000, 10000)
    test_cam.update(player)

    # Камера має впертися в нижній правий кут
    expected_x = -(3000 - SCREEN_WIDTH)
    expected_y = -(3000 - SCREEN_HEIGHT)

    assert test_cam.camera.x == expected_x
    assert test_cam.camera.y == expected_y
