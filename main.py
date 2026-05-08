import pygame
import sys
from settings import *
from Scenes.menu import MenuScene
from Scenes.game import GameScene
from Scenes.car_select import CarSelectScene
from Scenes.victory import VictoryScene

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Car Racing")
clock = pygame.time.Clock()

current_scene = "menu"

menu_scene = MenuScene(screen)
car_select_scene = CarSelectScene(screen)
game_scene = None
victory_scene = None

chosen_car_index = 0
chosen_color_index = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if current_scene == "menu":
            #Якщо зараз працю меню, то ми використовуємо функцію handle_event(), що прописана в menu.py
            result = menu_scene.handle_event(event)
            if result == "start":
                game_scene = GameScene(screen, chosen_car_index, chosen_color_index)
                current_scene = "game"
            elif result == "choice":
                current_scene = "choice"
            elif result == "exit":
                pygame.quit()
                sys.exit()

        elif current_scene == "choice":
            result = car_select_scene.handle_event(event)

            if result == "menu":
                current_scene = "menu"  # Повертаємось назад

            # Якщо result починається на "car_selected_"
            elif result and result.startswith("car_selected_"):
                # Розбиваємо рядок на частини. Наприклад: "car_selected_1_2"
                parts = result.split("_")
                chosen_car_index = int(parts[2])  # Номер машини
                chosen_color_index = int(parts[3])  # Номер кольору

                print(f"Обрано машину № {chosen_car_index}, колір № {chosen_color_index}")
                current_scene = "menu"

        elif current_scene == "game":
            result = game_scene.handle_event(event)
            if result == "menu": #Тобто якщо під час гри натиснуто кнопку Q, яка якраз таки і змінює result на menu, то ми виходимо в меню
                current_scene = "menu"

        elif current_scene == "victory":
            result = victory_scene.handle_event(event)
            if result == "menu": #Тут під час слайд-шоу для переможця програма очікує на натиснення Enter, який відповідає за зміну result на menu
                current_scene = "menu"
        # --- ВІДМАЛЬОВКА СЦЕН ---
    if current_scene == "menu":
        menu_scene.run()

    elif current_scene == "choice":
        car_select_scene.run()  # Відмальовуємо вибір авто

    elif current_scene == "game":
        result = game_scene.run() #До моменту перетину останнього кола current_scene = "game"
        if result == "menu":
            current_scene = "menu"
        elif result == "victory": #Коли гравець перетинає фініш, run() розуміє, що кола закінчилися, і повертає слово "victory". Код у main.py ловить це слово (elif result == "victory":).
            victory_scene = VictoryScene(screen)  # Створюємо сцену перемоги. Завантажуємо картинки і музику в пам'ять тільки тоді, коли вони реально знадобилися.
            current_scene = "victory" # Перемикаємо на презентацію

    elif current_scene == "victory":
        victory_scene.run()

    # Миттєво оновлює екран. Показує гравцеві повністю готовий новий кадр
    # (підміняє невидимий буфер на видимий екран), щоб уникнути мерехтіння.
    pygame.display.flip()
    clock.tick(FPS) #Обмежує кадри на 60 за секунду, аби наявність потужного ПК нічого не зруйнувало


