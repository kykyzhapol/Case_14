import pygame as pg
import ru_local as loc


def init_display(rows: int,
                 cols: int,
                 cell_size: int,
                 caption: str = 'Game of Life') -> tuple[pg.Surface, tuple]:
    '''
    The function initializes a Pygame window with specified dimensions and settings,
    and creates font objects of different sizes for text rendering.

    Args:
        rows (int): Number of rows in the game grid
        cols (int): Number of columns in the game grid
        cell_size (int): Size of each cell in pixels
        caption (str): Title of the game window (default is 'Game of Life')

    Returns:
        tuple[pg.Surface, tuple]: A tuple containing:
            - screen: Pygame surface object representing the game window
            - fonts: Tuple of three font objects (big, medium, small)
    '''
    # Initialize all pygame modules (display, draw, font, etc.)
    pg.init()

    # Calculate window dimensions
    width = cols * cell_size
    height = rows * cell_size
    # Create game window
    screen = pg.display.set_mode((width, height))

    # Set window title
    pg.display.set_caption(caption)

    # Create fonts objects
    font_big = pg.font.SysFont('Arial', 28)
    font_mid = pg.font.SysFont('Arial', 20)
    font_small = pg.font.SysFont('Arial', 18)
    fonts = (font_big, font_mid, font_small)

    return screen, fonts


def draw_grid(screen: pg.Surface,
              grid: list[list[int, int, int]],
              colors: dict[str : tuple],
              cell_size: int,
              show_grid: bool = True) -> None:
    '''
    The function renders the entire game grid including background,
    live cells, and optional grid lines.

    Args:
        screen (pg.Surface): Pygame surface to draw on
        grid (list[list[int, int, int]]): 2D list representing cell states
                                          (1 for alive, 0 for dead)
        color_alive (tuple[int, int, int]): RGB color for live cells
        color_dead (tuple[int, int, int]): RGB color for dead cells (background)
        color_grid (tuple[int, int, int]): RGB color for grid lines
        cell_size (int): Size of each cell in pixels
        show_grid (bool): Whether to draw grid lines (default is True)
    '''
    rows = len(grid)
    cols = len(grid[0])
    
    # Fill screen with dead cell color
    screen.fill(colors['dead'])

    # Draw live cells
    # First draw colored cells
    for row in range(rows):
        for col in range(cols):
            if grid[row][col]:
                rect = (col * cell_size, row * cell_size, cell_size, cell_size)
                pg.draw.rect(screen, colors['alive'], rect, width = 0)
    
    # Draw grid if user wants it
    if show_grid:
        # Draw vertical lines
        for col in range(cols + 1):
            start_line = (col * cell_size, 0)
            end_line = (col * cell_size, rows * cell_size)
            pg.draw.line(screen, colors['grid'], start_line, end_line)

        # Draw horizontal lines
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
            colors: dict[str : tuple]) -> None:
    '''
    The function renders text-based user interface information including
    game title, generation count, simulation speed, and game state.

    Args:
        screen (pg.Surface): Pygame surface to draw on
        fonts (tuple): Tuple containing three font objects (big, medium, small)
        generation (int): Current generation number
        speed (float): Simulation speed in milliseconds per generation
        running (bool): Game state
        name_game (str): Title of the game
        colors (dict[str : tuple]): Dictionary containing color values for UI elements
    '''
    font_big = fonts[0]
    font_mid = fonts[1]
    font_small = fonts[2]

    # Render information about: name, generation, speed, game state
    # Headers
    text_title = title
    text_gen = loc.gen.format(generation)
    text_speed = loc.speed.format(int(speed))
    text_status = loc.status.format('Запущена' if running else 'Пауза')

    # Create surfaces
    surf_title = font_big.render(text_title, True, colors['text'])
    surf_gen = font_mid.render(text_gen, True, colors['text'])
    surf_speed = font_small.render(text_speed, True, colors['text'])
    surf_status =font_small.render(text_status, True, colors['text'])

    # Text coordinates
    indent = 5
    x_pos = indent
    y_pos_title = indent
    y_pos_gen = y_pos_title + surf_title.get_height()
    y_pos_speed = y_pos_gen + surf_gen.get_height()
    y_pos_status = y_pos_speed + surf_speed.get_height()

    # Display surfaces with text
    screen.blit(surf_title, (x_pos, y_pos_title))
    screen.blit(surf_gen, (x_pos, y_pos_gen))
    screen.blit(surf_speed, (x_pos, y_pos_speed))
    screen.blit(surf_status, (x_pos, y_pos_status))    
    
    # Render information about: control keys
    control_keys = const.control_keys

    y_pos = indent
    for line in control_keys:
        # Создание поверхности
        control_key_surf = font_small.render(line, True, colors['text'])
        # Text coordinates
        x_pos = screen.get_width() - control_key_surf.get_width() - indent
        # Отображение поверхности
        screen.blit(control_key_surf, (x_pos, y_pos))
        
        y_pos += control_key_surf.get_height()


def get_cell_from_mouse(position: tuple[int, int],
                        rows: int,
                        cols: int,
                        cell_size: int) -> tuple[int, int] | None:
    '''
    The function converts mouse coordinates to grid cell indices.

    Args:
        position (tuple[int, int]): Mouse coordinates (x, y) in pixels
        rows (int): Number of rows in the grid
        cols (int): Number of columns in the grid
        cell_size (int): Size of each cell in pixels

    Returns:
        tuple[int, int] | None: Cell indices (row, col) if within grid bounds,
                                None if outside the grid
    '''
    x, y = position
    row = y // cell_size
    col = x // cell_size

    if 0 <= row <= rows and 0 <= col <= cols:
        return (row, col)


def handle_color_scheme(colors: dict) -> None:
    '''
    The function cycles through available color themes in the colors dictionary.
    When called, it switches to the next predefined color scheme.
    This function is typically called when the user presses the 'N' key.

    Args:
        colors (dict): Dictionary containing color values for different UI elements
                      ('alive', 'dead', 'grid', 'text')
                      The dictionary is modified in place.
    '''
    color_themes = loc.color_themes
    # Get current color theme as a tuple of values to compare
    current_values = tuple(colors.items())

    # Find current theme index and switch to next one
    current_index = -1
    for i, theme in enumerate(color_themes):
        # Check to find the current theme among color_themes
        if tuple(theme.items()) == current_values:
            current_index = i
            break
    
    # Switch to next theme (or first if current not found or is last)
    next_index = (current_index + 1) % len(color_themes)
    next_theme = color_themes[next_index]
    
    # Update colors dictionary with new theme
    for key, value in next_theme.items():
        colors[key] = value
