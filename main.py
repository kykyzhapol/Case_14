"""
Conway's Game of Life simulation with Pygame.

Features:
- Choose initial grid size and pattern (random, load from file, or predefined figures)
- Interactive controls: space (pause/play), s/right (step), r (random), c (clear),
  l (load), f (save), +/- (speed), 1-4 (themes), q (quit), mouse click (toggle cells)
- Displays generation count, simulation speed, and color themes.
"""

import json
import sys

import pygame as pg

import constants as con
import display as dis
import game_logic as logic
import grid_io as io
import ru_local as loc  # Russian localization strings

# ==============================================================================
# Figure loading and placement
# ==============================================================================


def parse_figures(filepath="start_figur.json"):
    """
    Load predefined figures from a JSON file.

    The file should contain a dictionary with figure names as keys,
    each value is a list: [rows, cols, matrix].

    Args:
        filepath (str): Path to the JSON file. Default "start_figur.json".

    Returns:
        dict: A dictionary mapping figure names to tuples (rows, cols, matrix).
              Returns empty dict if file is not found or an error occurs.
    """
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)  # Load JSON data into a Python dictionary
        result = {}
        # Process each figure in the loaded data
        for name, item in data.items():
            # The matrix is stored at index 2 in the list
            matrix = item[2]
            rows = len(matrix)
            cols = len(matrix[0]) if rows else 0
            result[name] = (rows, cols, matrix)
        return result
    except FileNotFoundError:
        # Handle missing file gracefully
        print(f"File {filepath} not found. Using empty figures.")
        return {}
    except Exception as e:
        # Catch any other errors during loading
        print(f"Error loading {filepath}: {e}")
        return {}


def place_figure(grid, rows, cols, figure_rows, figure_cols, figure_matrix):
    """
    Place a figure in the centre of the grid.

    Args:
        grid (list of list of int): The game grid (0 = dead, 1 = alive).
        rows (int): Number of rows in the grid.
        cols (int): Number of columns in the grid.
        figure_rows (int): Height of the figure matrix.
        figure_cols (int): Width of the figure matrix.
        figure_matrix (list of list of int): The figure pattern (1 = alive cell).

    Returns:
        list of list of int: The updated grid with the figure placed.
    """
    # Calculate starting position to center the figure
    start_row = (rows - figure_rows) // 2
    start_col = (cols - figure_cols) // 2
    # Iterate through each cell of the figure
    for r in range(figure_rows):
        for c in range(figure_cols):
            if figure_matrix[r][c]:  # Only place live cells
                grid[start_row + r][start_col + c] = 1
    return grid


# ------------------------------------------------------------------------------
# Initial setup menu
# ------------------------------------------------------------------------------


def initial_setup():
    """
    Display a menu to choose grid size and initial configuration.

    Allows the user to:
    - Adjust grid size with +/- keys.
    - Select a starting pattern (random, load from file, or a predefined figure).
    - Press Enter to start the simulation.

    Returns:
        tuple: (grid, rows, cols) where grid is a 2D list of 0/1.
    """
    pg.init()
    screen = pg.display.set_mode((800, 600))
    pg.display.set_caption(loc.SETUP_TITLE)   # localized caption
    clock = pg.time.Clock()
    font = pg.font.Font(None, 36)
    small_font = pg.font.Font(None, 28)

    # Define some colors for the menu
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (200, 200, 200)
    HIGHLIGHT = (100, 200, 100)

    # Default grid size is 100x100
    rows = cols = 100
    # Load available figures from the JSON file
    figures = parse_figures()
    # Build list of menu options: random, load file, then all figure names
    options = [loc.OPTION_RANDOM, loc.OPTION_LOAD_FILE] + list(figures.keys())
    selected_option = 0  # Index of the currently highlighted option

    def draw_text(text, x, y, color=WHITE, font_obj=font, centered=False):
        """Helper to draw text on the screen."""
        surf = font_obj.render(text, True, color)
        if centered:
            rect = surf.get_rect(center=(x, y))
            screen.blit(surf, rect)
        else:
            screen.blit(surf, (x, y))

    def draw_menu():
        """Draw the menu screen."""
        screen.fill(BLACK)
        # Title
        draw_text(loc.SETUP_TITLE, 400, 50, WHITE, font, centered=True)
        # Show current grid size
        draw_text(loc.SETUP_GRID_SIZE.format(rows, cols), 400, 150,
                  WHITE, font, centered=True)

        # Draw each menu option
        y_start = 250
        for i, opt in enumerate(options):
            color = HIGHLIGHT if i == selected_option else WHITE
            draw_text(opt, 400, y_start + i * 40, color, font, centered=True)

        # Hint to press Enter
        draw_text(loc.PRESS_ENTER, 400, 550, GRAY, small_font, centered=True)
        pg.display.flip()

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    # User selected an option; create the grid accordingly
                    opt = options[selected_option]
                    if opt == loc.OPTION_RANDOM:
                        # Random grid with ~20% alive cells
                        grid = io.random_grid(rows, cols, prob=0.2)
                    elif opt == loc.OPTION_LOAD_FILE:
                        try:
                            grid = io.load_grid_from_file("saved_grid.txt")
                            # Verify loaded grid dimensions match current size
                            if len(grid) != rows or len(grid[0]) != cols:
                                print(loc.FILE_SIZE_MISMATCH)
                                grid = io.random_grid(rows, cols, prob=0.2)
                        except Exception as e:
                            print(loc.FILE_LOAD_ERROR.format(e))
                            grid = io.random_grid(rows, cols, prob=0.2)
                    else:  # it's a figure name
                        fig_rows, fig_cols, fig_matrix = figures[opt]
                        grid = io.create_empty_grid(rows, cols)
                        grid = place_figure(grid, rows, cols,
                                            fig_rows, fig_cols, fig_matrix)
                    # Exit setup and return to main simulation
                    return grid, rows, cols

                elif event.key == pg.K_UP:
                    # Move selection up
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == pg.K_DOWN:
                    # Move selection down
                    selected_option = (selected_option + 1) % len(options)

                # Adjust grid size with +/- keys (clamped between 100 and 120)
                elif event.key in (pg.K_PLUS, pg.K_EQUALS):
                    rows = cols = min(120, rows + 1)
                elif event.key == pg.K_MINUS:
                    rows = cols = max(100, rows - 1)

        draw_menu()
        clock.tick(30)  # Limit to 30 FPS for the menu


# ==============================================================================
# Main simulation loop and event handling
# ==============================================================================


def main():
    """Main function: runs the simulation after initial setup."""
    # Get initial grid and dimensions from the setup menu
    grid, rows, cols = initial_setup()
    CELL_SIZE = 10          # Size of each cell in pixels
    SPEED = 10              # Default frames per second (generations per second)
    SHOW_GRID = True        # Whether to draw grid lines

    current_theme_key = 2   # Start with dark theme (index 2 in color_themes)
    colors = con.color_themes[current_theme_key]

    pg.init()
    # Initialize the display; we only need the screen object
    screen, *rest = dis.init_display(rows, cols, CELL_SIZE)   # unpack extra
    clock = pg.time.Clock()

    # Create fonts of different sizes for UI text
    font_big = pg.font.Font(None, 48)
    font_medium = pg.font.Font(None, 36)
    font_small = pg.font.Font(None, 24)
    fonts = (font_big, font_medium, font_small)

    # Simulation state variables
    running = True           # Main loop flag
    simulation_running = True  # Whether the game is evolving automatically
    generation = 0           # Current generation count
    speed = SPEED            # Current FPS (can be changed by user)

    while running:
        # Process all events and update state
        grid, simulation_running, speed, generation, running, colors = handle_events(
            grid, simulation_running, speed, generation, running,
            CELL_SIZE, colors, con.color_themes)

        # If simulation is running, compute next generation
        if simulation_running:
            grid = logic.next_generation(grid)
            generation += 1

        # Draw the grid and UI
        dis.draw_grid(screen, grid, colors, CELL_SIZE, SHOW_GRID)
        dis.draw_ui(screen, fonts, generation, speed,
                    simulation_running, loc.TITLE_MAIN, colors)
        pg.display.flip()   # Update the screen
        clock.tick(speed)   # Maintain the desired FPS

    pg.quit()
    sys.exit()


def handle_events(grid, simulation_running, speed, generation, running,
                  cell_size, current_colors, color_themes):
    """
    Process all Pygame events and update the simulation state accordingly.

    Args:
        grid (list of list of int): Current grid state.
        simulation_running (bool): Whether the simulation is actively evolving.
        speed (int): Frames per second (generations per second when running).
        generation (int): Current generation count.
        running (bool): Whether the main loop should continue.
        cell_size (int): Size of each cell in pixels.
        current_colors (dict): Current color theme dictionary.
        color_themes (dict): All available color themes.

    Returns:
        tuple: Updated (grid, simulation_running, speed, generation, running,
               current_colors)
    """
    rows = len(grid)
    cols = len(grid[0]) if rows else 0

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        elif event.type == pg.KEYDOWN:
            # Space: toggle simulation running
            if event.key == pg.K_SPACE:
                simulation_running = not simulation_running

            # s or right arrow: step one generation (only when paused)
            elif event.key in (pg.K_s, pg.K_RIGHT):
                if not simulation_running:
                    grid = logic.next_generation(grid)
                    generation += 1

            # r: randomize the grid
            elif event.key == pg.K_r:
                grid = io.random_grid(rows, cols, prob=0.2)
                generation = 0

            # c: clear the grid (all dead cells)
            elif event.key == pg.K_c:
                grid = io.create_empty_grid(rows, cols)
                generation = 0

            # l: load grid from file
            elif event.key == pg.K_l:
                filename = "saved_grid.txt"
                try:
                    new_grid = io.load_grid_from_file(filename)
                    # Check that loaded grid matches current dimensions
                    if len(new_grid) == rows and all(len(row) == cols for row in new_grid):
                        grid = new_grid
                        generation = 0
                        print(loc.GRID_LOADED.format(filename))
                    else:
                        print(loc.FILE_SIZE_MISMATCH)
                except Exception as e:
                    print(loc.FILE_LOAD_ERROR.format(e))

            # f: save current grid to file
            elif event.key == pg.K_f:
                filename = "saved_grid.txt"
                io.save_grid_to_file(grid, filename)
                print(loc.GRID_SAVED.format(filename))

            # + or = : increase speed (max 60)
            elif event.key in (pg.K_PLUS, pg.K_EQUALS):
                speed = min(speed + 1, 60)

            # - : decrease speed (min 1)
            elif event.key == pg.K_MINUS:
                speed = max(speed - 1, 1)

            # Theme selection keys 1-4
            elif event.key == pg.K_1:
                current_colors = color_themes[1]
                print(loc.THEME_LIGHT)
            elif event.key == pg.K_2:
                current_colors = color_themes[2]
                print(loc.THEME_DARK)
            elif event.key == pg.K_3:
                current_colors = color_themes[3]
                print(loc.THEME_COLD)
            elif event.key == pg.K_4:
                current_colors = color_themes[4]
                print(loc.THEME_WARM)

            # q: quit the program
            elif event.key == pg.K_q:
                running = False

        elif event.type == pg.MOUSEBUTTONDOWN:
            # Left mouse button: toggle cell state
            if event.button == 1:
                pos = pg.mouse.get_pos()
                cell = dis.get_cell_from_mouse(pos, rows, cols, cell_size)
                if cell is not None:
                    row, col = cell
                    if 0 <= row < rows and 0 <= col < cols:
                        # Flip the cell: 0 becomes 1, 1 becomes 0
                        new_value = 0 if grid[row][col] else 1
                        grid = io.set_cell(grid, row, col, new_value)

    return (grid, simulation_running, speed, generation,
            running, current_colors)


if __name__ == "__main__":
    main()
