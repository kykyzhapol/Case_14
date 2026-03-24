'''
aka, role B
'''


def count_live_neighbors(grid: list[list[int]], row: int, col: int) -> int:
    '''
    The function counts the number of live neighbors for a given cell,
    using wrap-around boundary conditions.

    Args:
        grid (list[list[int]]): A 2D list representing the grid
        row (int): Row index of the cell
        col (int): Column index of the cell

    Returns:
        int: Number of live neighbors around the specified cell
    '''
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
    '''
    The function calculates the next generation of the Game of Life
    based on Conway's rules:
    - A live cell with 2 or 3 live neighbors survives
    - A dead cell with exactly 3 live neighbors becomes alive
    - All other cells die or remain dead

    Args:
        grid (list[list[int]]): Current generation grid

    Returns:
        list[list[int]]: New grid representing the next generation
                         (original grid remains unchanged)
    '''
    new_grid = [row[:] for row in grid]
    
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
        '''
    The function applies toroidal (wrap-around) boundary conditions
    to convert coordinates that may be outside the grid bounds
    into valid coordinates within the grid.

    Args:
        grid (list[list[int]]): A 2D list representing the grid
        row (int): Row index (may be negative or exceed grid bounds)
        col (int): Column index (may be negative or exceed grid bounds)

    Returns:
        tuple[int, int]: Valid coordinates (row, col) within the grid bounds
    '''
    row_1 = row % len(grid)
    col_1 = col % len(grid[0])
    cordinates = (row_1, col_1)

    return cordinates
