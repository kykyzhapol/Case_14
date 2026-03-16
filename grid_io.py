import pygame
'''
aka, role A
Ok, how I see grid (like a matrix)
example:
0 0 1 0 1 - list
0 1 0 1 1
0 1 1 1 0
1 0 1 0 0
1 0 0 1 1
grid is list of lists
'''


def create_empty_grid(rows: int, cols: int) -> list[list[int]]:
    """Создаёт пустую сетку (все клетки мертвы)."""

def random_grid(rows: int, cols: int, prob: float = 0.5) -> list[list[int]]:
    """Заполняет сетку случайными значениями с заданной вероятностью жизни."""

def load_grid_from_file(filename: str) -> list[list[int]]:
    """Читает сетку из текстового файла. Формат файла обсуждается командой."""

def save_grid_to_file(grid: list[list[int]], filename: str) -> None:
    """Сохраняет сетку в файл."""

def set_cell(grid: list[list[int]], row: int, col: int, value: int) -> None:
    """Устанавливает состояние конкретной клетки (понадобится для рисования мышкой)."""
