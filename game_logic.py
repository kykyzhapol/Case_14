'''
aka, role B
'''


def count_live_neighbors(grid: list[list[int]], row: int, col: int) -> int:
    """Возвращает количество живых соседей для клетки (row, col) с учётом границ."""
    summ = 0
    n = len(grid)
    m = len(grid[0])

    row_1 = grid[(row - 1) % n]
    summ += row_1[(col - 1) % m]
    summ += row_1[col]
    summ += row_1[(col + 1) % m]

    row_2 = grid[row]
    summ += row_2[(col - 1) % m]
    summ += row_2[(col + 1) % m]

    row_3 = grid[(row - 1) % n]
    summ += row_3[(col - 1) % m]
    summ += row_3[col]
    summ += row_3[(col + 1) % m]

    return summ


def next_generation(grid: list[list[int]]) -> list[list[int]]:
    """Вычисляет следующее поколение и возвращает новую сетку (не изменяя исходную)."""

    new_grid = grid
    n = len(grid)
    m = len(grid[0])
    for row in range(n):
        for col in range(m):
            neighbors = count_live_neighbors(grid, row, col)
            if (neighbors >= 2) and (neighbors <= 3):
                new_grid[row][col] = 1
            else:
                new_grid[row][col] = 0

    return new_grid


def apply_boundary_condition(grid: list[list[int]], row: int, col: int) -> tuple[int, int]:
    """Опционально: преобразует координаты с учётом границ (для тора)."""

    row_1 = row % len(grid)
    col_1 = col % len(grid[0])
    cordinates = (row_1, col_1)

    return cordinates
