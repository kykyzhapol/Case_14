import display as dis
import game_logic as logic
import grid_io as io

import pygame as pg
import sys
from typing import Tuple, Optional

# Import your existing functions (placeholders)
# from your_module import create_empty_grid, random_grid, load_grid_from_file, save_grid_to_file,
#     set_cell, count_live_neighbors, next_generation, init_display, draw_grid, get_cell_from_mouse, draw_ui

# ==============================================================================
# Main function
# ==============================================================================

def main():
    """Главная функция программы."""
    # 1. Параметры
    ROWS, COLS = 50, 70
    CELL_SIZE = 10
    INIT_PROB = 0.2
    SPEED = 10
    SHOW_GRID = True
    TITLE = "Game of Life"

    # 2. Цвета
    COLORS = {
        'alive': (0, 255, 0),  # зелёный
        'dead': (0, 0, 0),  # чёрный
        'grid': (40, 40, 40),  # тёмно-серый
        'text': (255, 255, 255)  # белый (для текста интерфейса)
    }

    # 3. Инициализация Pygame
    pg.init()
    screen, *rest = dis.init_display(ROWS, COLS, CELL_SIZE)   # screen — Surface
    clock = pg.time.Clock()


    # Создаём шрифты: большой, средний, малый
    font_big = pg.font.Font(None, 48)      # для заголовка
    font_medium = pg.font.Font(None, 36)   # для поколения и скорости
    font_small = pg.font.Font(None, 24)    # для подсказок
    fonts = (font_big, font_medium, font_small)

    # Создание начальной сетки
    grid = io.random_grid(ROWS, COLS, INIT_PROB)

    # Состояние игры
    running = True
    simulation_running = True
    generation = 0
    speed = SPEED

    # 4. Главный цикл
    while running:
        # Обработка событий
        grid, simulation_running, speed, generation, running = handle_events(
            grid, simulation_running, speed, generation, running, CELL_SIZE
        )

        if simulation_running:
            grid = logic.next_generation(grid)
            generation += 1

        # Отрисовка
        dis.draw_grid(screen, grid, COLORS, CELL_SIZE, SHOW_GRID)
        dis.draw_ui(screen, fonts, generation, speed, simulation_running, TITLE, COLORS)
        pg.display.flip()

        clock.tick(speed)

    pg.quit()
    sys.exit()
# ==============================================================================
# Event handling
# ==============================================================================

def handle_events(grid: list[list[int]],
                  simulation_running: bool,
                  speed: float,
                  generation: int,
                  running: bool,
                  cell_size: int
                  ) -> tuple[list[list[int]], bool, float, int, bool]:
    """
    Обрабатывает события Pygame и обновляет состояние игры.

    Аргументы:
        grid: текущая сетка.
        simulation_running: флаг паузы (True – симуляция идёт).
        speed: скорость (поколений в секунду).
        generation: текущее поколение.
        running: флаг продолжения работы программы.
        cell_size: размер клетки в пикселях.

    Возвращает:
        кортеж (grid, simulation_running, speed, generation, running)
        с обновлёнными значениями.
    """
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        elif event.type == pg.KEYDOWN:
            # Пробел – пауза / продолжение
            if event.key == pg.K_SPACE:
                simulation_running = not simulation_running

            # Стрелки вверх/вниз – изменение скорости
            elif event.key == pg.K_UP:
                speed = min(speed + 1, 60)
            elif event.key == pg.K_DOWN:
                speed = max(speed - 1, 1)

            # Клавиша 'r' – случайная переинициализация сетки
            elif event.key == pg.K_r:
                rows = len(grid)
                cols = len(grid[0]) if rows else 0
                grid = io.random_grid(rows, cols, prob=0.2)
                generation = 0

            # Клавиша 'c' – очистка сетки
            elif event.key == pg.K_c:
                rows = len(grid)
                cols = len(grid[0]) if rows else 0
                grid = io.create_empty_grid(rows, cols)
                generation = 0

            # Клавиша 's' – сохранение
            elif event.key == pg.K_s:
                filename = "saved_grid.txt"
                io.save_grid_to_file(grid, filename)
                print(f"Сетка сохранена в {filename}")

            # Клавиша 'l' – загрузка
            elif event.key == pg.K_l:
                filename = "saved_grid.txt"
                try:
                    new_grid = io.load_grid_from_file(filename)
                    rows, cols = len(grid), len(grid[0])
                    if len(new_grid) == rows and all(len(row) == cols for row in new_grid):
                        grid = new_grid
                        generation = 0
                        print(f"Сетка загружена из {filename}")
                    else:
                        print("Ошибка: размеры загружаемой сетки не совпадают")
                except Exception as e:
                    print(f"Не удалось загрузить файл: {e}")


        elif event.type == pg.MOUSEBUTTONDOWN:

            if event.button == 1:  # левая кнопка

                pos = pg.mouse.get_pos()

                rows = len(grid)

                cols = len(grid[0]) if rows else 0

                # Передаём pos, rows, cols, cell_size (порядок зависит от реализации в display.py)

                cell = dis.get_cell_from_mouse(pos, rows, cols, cell_size)

                if cell is not None:

                    row, col = cell

                    if 0 <= row < rows and 0 <= col < cols:
                        new_value = 0 if grid[row][col] else 1

                        grid = io.set_cell(grid, row, col, new_value)

    return grid, simulation_running, speed, generation, running

# ==============================================================================
# If this script is run directly
# ==============================================================================

if __name__ == "__main__":
    main()