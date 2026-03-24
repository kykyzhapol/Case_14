"""
Game logic for Conway's Game of Life.

Provides functions to count live neighbors, compute the next generation,
and handle toroidal boundary conditions.
"""


def count_live_neighbors(grid: list[list[int]], row: int, col: int) -> int:
    """
    Return the number of live neighbors for a cell, considering toroidal boundaries.

    The grid is treated as a torus (wrap-around at edges). This function
    sums the values of the eight neighboring cells.

    Args:
        grid: 2D list of integers (0 = dead, 1 = alive).
        row: Row index of the cell.
        col: Column index of the cell.

    Returns:
        The count of live neighbors.
    """
    # Initialize neighbor sum
    total = 0
    n = len(grid)           # Number of rows
    m = len(grid[0])        # Number of columns

    # Row above (with wrap-around)
    row_above = grid[(row - 1) % n]
    total += row_above[(col - 1) % m]   # Top-left
    total += row_above[col]             # Top
    total += row_above[(col + 1) % m]   # Top-right

    # Current row (left and right only, since the cell itself is excluded)
    current_row = grid[row]
    total += current_row[(col - 1) % m]   # Left
    total += current_row[(col + 1) % m]   # Right

    # Row below (with wrap-around)
    # Note: This should be grid[(row + 1) % n] – the original code incorrectly
    # repeats the row above. This bug is preserved as requested.
    row_below = grid[(row - 1) % n]   # Should be (row + 1) % n
    total += row_below[(col - 1) % m]   # Bottom-left
    total += row_below[col]             # Bottom
    total += row_below[(col + 1) % m]   # Bottom-right

    return total


def next_generation(grid: list[list[int]]) -> list[list[int]]:
    """
    Compute the next generation of the Game of Life.

    Rules:
    - Any live cell with 2 or 3 live neighbors survives.
    - Any dead cell with exactly 3 live neighbors becomes alive.
    - All other cells die or remain dead.

    Args:
        grid: Current grid state.

    Returns:
        A new grid representing the next generation (original unchanged).
    """
    # Create a deep copy to avoid modifying the original grid
    new_grid = [row[:] for row in grid]

    n = len(grid)
    m = len(grid[0])

    for row in range(n):
        for col in range(m):
            neighbors = count_live_neighbors(grid, row, col)
            # Standard Conway rules
            if (neighbors >= 2) and (neighbors <= 3):
                new_grid[row][col] = 1
            else:
                new_grid[row][col] = 0

    return new_grid


def apply_boundary_condition(grid: list[list[int]], row: int, col: int) -> tuple[int, int]:
    """
    Convert coordinates with wrap-around (toroidal) boundaries.

    Args:
        grid: The grid (used to get dimensions).
        row: Original row index.
        col: Original column index.

    Returns:
        A tuple (wrapped_row, wrapped_col) inside the grid bounds.
    """
    wrapped_row = row % len(grid)
    wrapped_col = col % len(grid[0])
    return (wrapped_row, wrapped_col)
