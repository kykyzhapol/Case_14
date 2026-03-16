'''
aka, role B
'''


def count_live_neighbors(grid: list[list[int]], row: int, col: int) -> int:
    """Возвращает количество живых соседей для клетки (row, col) с учётом границ."""

def next_generation(grid: list[list[int]]) -> list[list[int]]:
    """Вычисляет следующее поколение и возвращает новую сетку (не изменяя исходную)."""

def apply_boundary_condition(grid: list[list[int]], row: int, col: int) -> tuple[int, int]:
    """Опционально: преобразует координаты с учётом границ (для тора)."""
