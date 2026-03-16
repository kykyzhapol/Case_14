'''
aka, role C
'''


def init_display(rows: int, cols: int, cell_size: int = 20) -> tuple:
    """
    Инициализирует окно Pygame, задаёт размеры.
    Возвращает объект экрана и, возможно, другие параметры.
    """

def draw_grid(screen, grid: list[list[int]], generation: int, speed: float) -> None:
    """Отрисовывает всю сетку: цвет фона для мёртвых, цвет для живых, линии сетки (опционально)."""

def get_cell_from_mouse(pos: tuple[int, int], cell_size: int) -> tuple[int, int] | None:
    """По координатам мыши возвращает индексы клетки (row, col) или None, если вне сетки."""

def draw_ui(screen, generation: int, speed: float, running: bool) -> None:
    """Отрисовывает текстовую информацию (поколение, скорость, статус паузы)."""

def handle_color_scheme(alive_color, dead_color, grid_color) -> None:
    """Настройка цветов (опционально)."""
