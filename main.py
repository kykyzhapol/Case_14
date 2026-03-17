import pygame
import random
import display as dis
import game_logic as logic
import grid_io as grid_mod

def main():
    # Настройки
    rows, cols = 40, 40
    cell_size = 20
    speed = 0.1  # задержка между поколениями в секундах
    running = False  # флаг автоматической симуляции
    generation = 0

    # Инициализация
    grid = grid_mod.random_grid(rows, cols)
    screen, clock = dis.init_display(rows, cols, cell_size)

    # Главный цикл
    while True:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            # Здесь вызовы функций обработки клавиш и мыши, которые изменяют grid, running и т.д.

        # Логика
        if running:
            grid = logic.next_generation(grid)
            generation += 1

        # Отрисовка
        dis.draw_grid(screen, grid, generation, speed)
        dis.draw_ui(screen, generation, speed, running)
        pygame.display.flip()

        # Задержка
        pygame.time.delay(int(speed * 1000))