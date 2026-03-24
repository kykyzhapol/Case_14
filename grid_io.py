"""
Grid input/output operations for Conway's Game of Life.

Provides functions to create, randomize, load, save, and modify the game grid.
Grid is represented as a list of lists of integers (0 = dead, 1 = alive).
"""

import json
import random


def create_empty_grid(rows: int, cols: int) -> list[list[int]]:
    """
    Create an empty grid with all cells dead.

    Args:
        rows: Number of rows in the grid.
        cols: Number of columns in the grid.

    Returns:
        A 2D list filled with zeros.
    """
    # List comprehension to create rows of zeros
    empty_grid = [[0 for _ in range(cols)] for _ in range(rows)]
    return empty_grid


def random_grid(rows: int, cols: int, prob: float = 0.5) -> list[list[int]]:
    """
    Generate a grid with random cell states.

    Each cell has probability `prob` to be alive (1) and (1 - prob) to be dead (0).

    Args:
        rows: Number of rows in the grid.
        cols: Number of columns in the grid.
        prob: Probability of a cell being alive (default 0.5).

    Returns:
        A 2D list with random alive/dead cells.
    """
    # For each row, create a list of random choices with given probabilities
    rand_grid = [random.choices([1, 0], [prob, 1 - prob], k=cols)
                 for _ in range(rows)]
    return rand_grid


def load_grid_from_file(filename: str) -> list[list[int]]:
    """
    Load a grid from a JSON file.

    The file should contain a 2D list of integers (0 or 1).

    Args:
        filename: Path to the JSON file.

    Returns:
        The loaded grid as a list of lists.
    """
    with open(filename, 'r', encoding='utf-8') as data:
        grid = json.load(data)
    return grid


def save_grid_to_file(grid: list[list[int]], filename: str) -> None:
    """
    Save the grid to a JSON file.

    Args:
        grid: The grid to save.
        filename: Path to the output file.
    """
    with open(filename, 'w', encoding='utf-8') as data:
        json.dump(grid, data)


def set_cell(grid: list[list[int]], row: int, col: int, value: int) -> list[list[int]]:
    """
    Return a new grid with the specified cell changed to the given value.

    The original grid is not modified. If the cell already has the desired value,
    the original grid is returned unchanged.

    Args:
        grid: Original grid.
        row: Row index of the cell.
        col: Column index of the cell.
        value: New cell value (0 or 1).

    Returns:
        A new grid with the updated cell.

    Raises:
        ValueError: If row or col indices are out of bounds.
    """
    # Validate indices
    if not (0 <= row < len(grid) and 0 <= col < len(grid[0])):
        raise ValueError("Invalid cell coordinates")

    # No change needed if value already matches
    if grid[row][col] == value:
        return grid

    # Create shallow copy of the grid
    new_grid = grid[:]
    # Build a new row with the updated column value
    new_row = grid[row][:col] + [value] + grid[row][col + 1:]
    new_grid[row] = new_row

    return new_grid
