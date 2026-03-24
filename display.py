"""
Display module for Conway's Game of Life.

Provides functions to initialize the Pygame window, draw the grid,
render UI text, and convert mouse coordinates to grid indices.
"""

import pygame as pg
import ru_local as loc  # Russian localization constants


def init_display(rows: int,
                 cols: int,
                 cell_size: int,
                 caption: str = 'Game of Life') -> tuple[pg.Surface, tuple]:
    """
    Initialize the Pygame window and create font objects.

    Args:
        rows: Number of rows in the game grid.
        cols: Number of columns in the game grid.
        cell_size: Size of each cell in pixels.
        caption: Title of the game window (default 'Game of Life').

    Returns:
        A tuple containing:
            - screen: Pygame surface representing the game window.
            - fonts: Tuple of three font objects (big, medium, small).
    """
    pg.init()
    width = cols * cell_size
    height = rows * cell_size
    screen = pg.display.set_mode((width, height))
    pg.display.set_caption(caption)

    # Create three font sizes for different UI elements
    font_big = pg.font.SysFont('Arial', 28)
    font_mid = pg.font.SysFont('Arial', 20)
    font_small = pg.font.SysFont('Arial', 18)
    fonts = (font_big, font_mid, font_small)

    return screen, fonts


def draw_grid(screen: pg.Surface,
              grid: list[list[int]],
              colors: dict,
              cell_size: int,
              show_grid: bool = True) -> None:
    """
    Render the entire game grid including background, live cells, and optional grid lines.

    Args:
        screen: Pygame surface to draw on.
        grid: 2D list representing cell states (1 for alive, 0 for dead).
        colors: Dictionary with keys 'alive', 'dead', 'grid' containing RGB color tuples.
        cell_size: Size of each cell in pixels.
        show_grid: Whether to draw grid lines (default True).
    """
    rows = len(grid)
    cols = len(grid[0])

    # Fill background with dead cell color
    screen.fill(colors['dead'])

    # Draw live cells
    for row in range(rows):
        for col in range(cols):
            if grid[row][col]:
                rect = (col * cell_size, row * cell_size, cell_size, cell_size)
                pg.draw.rect(screen, colors['alive'], rect, width=0)

    # Draw grid lines if requested
    if show_grid:
        # Vertical lines
        for col in range(cols + 1):
            start_line = (col * cell_size, 0)
            end_line = (col * cell_size, rows * cell_size)
            pg.draw.line(screen, colors['grid'], start_line, end_line)
        # Horizontal lines
        for row in range(rows + 1):
            start_line = (0, row * cell_size)
            end_line = (cols * cell_size, row * cell_size)
            pg.draw.line(screen, colors['grid'], start_line, end_line)


def draw_ui(screen: pg.Surface,
            fonts: tuple,
            generation: int,
            speed: float,
            running: bool,
            title: str,
            colors: dict) -> None:
    """
    Render text-based user interface (generation count, speed, status, controls).

    Args:
        screen: Pygame surface to draw on.
        fonts: Tuple of three font objects (big, medium, small).
        generation: Current generation number.
        speed: Simulation speed in frames per second.
        running: Game state (True = running, False = paused).
        title: Title of the game.
        colors: Dictionary with key 'text' containing RGB color tuple.
    """
    font_big, font_mid, font_small = fonts

    # Game title (top left)
    surf_title = font_big.render(title, True, colors['text'])
    screen.blit(surf_title, (5, 5))

    # Generation count (below title)
    gen_text = loc.GENERATION_LABEL.format(generation)
    surf_gen = font_mid.render(gen_text, True, colors['text'])
    screen.blit(surf_gen, (5, 5 + surf_title.get_height()))

    # Speed (below generation)
    speed_text = loc.SPEED_LABEL.format(int(speed))
    surf_speed = font_small.render(speed_text, True, colors['text'])
    screen.blit(surf_speed, (5, 5 + surf_title.get_height() + surf_gen.get_height()))

    # Status (below speed)
    status_str = loc.STATUS_RUNNING if running else loc.STATUS_PAUSED
    status_text = loc.STATUS_LABEL.format(status_str)
    surf_status = font_small.render(status_text, True, colors['text'])
    y_status = (5 + surf_title.get_height() + surf_gen.get_height() +
                surf_speed.get_height())
    screen.blit(surf_status, (5, y_status))

    # Control instructions (right side, aligned to the right edge)
    indent = 5
    y_pos = indent
    for line in loc.CONTROLS:
        surf_ctrl = font_small.render(line, True, colors['text'])
        x_pos = screen.get_width() - surf_ctrl.get_width() - indent
        screen.blit(surf_ctrl, (x_pos, y_pos))
        y_pos += surf_ctrl.get_height()


def get_cell_from_mouse(position: tuple[int, int],
                        rows: int,
                        cols: int,
                        cell_size: int) -> tuple[int, int] | None:
    """
    Convert mouse coordinates to grid cell indices.

    Args:
        position: Mouse coordinates (x, y) in pixels.
        rows: Number of rows in the grid.
        cols: Number of columns in the grid.
        cell_size: Size of each cell in pixels.

    Returns:
        Cell indices (row, col) if inside the grid, otherwise None.
    """
    x, y = position
    row = y // cell_size
    col = x // cell_size

    if 0 <= row < rows and 0 <= col < cols:
        return (row, col)
    return None
