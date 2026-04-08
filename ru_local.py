# ru_local.py
# Russian localization constants (all caps)

# Setup menu
SETUP_TITLE = "Игра «Жизнь» – Настройка"
SETUP_GRID_SIZE = "Размер сетки: {} x {} (используйте +/- для изменения)"
OPTION_RANDOM = "Случайно"
OPTION_LOAD_FILE = "Загрузить из файла"
PRESS_ENTER = "Нажмите ENTER для старта"

# Main window
TITLE_MAIN = "Игра «Жизнь»"

# UI labels
GENERATION_LABEL = "Поколение: {}"
SPEED_LABEL = "Скорость: {} FPS"
STATUS_LABEL = "Состояние игры: {}"
STATUS_RUNNING = "Запущена"
STATUS_PAUSED = "На паузе"

# Console messages
FILE_SIZE_MISMATCH = "Несоответствие размеров сетки. Используется случайная."
FILE_LOAD_ERROR = "Не удалось загрузить файл: {}. Используется случайная."
GRID_LOADED = "Сетка загружена из {}"
GRID_SAVED = "Сетка сохранена в {}"
THEME_LIGHT = "Тема: светлая"
THEME_DARK = "Тема: тёмная"
THEME_COLD = "Тема: холодная"
THEME_WARM = "Тема: тёплая"

# Help / control keys (only keyboard shortcuts, no language switch, no mouse)
CONTROLS  = ['Space: запуск/пауза',
                'S: шаг на одно поколение',
                'R: сброс конфигурации к начальной',
                'C: очистить все',
                'L: загрузить конфигурацию из файла',
                'F: сохранить текущую конфигурацию в файл',
                '+/-:  увеличить/уменьшить скорость симуляции',
                'Q: выход',
                'N: следующая цветовая схема',
                'LMB: сделать клетку живой',
                'RMB: сделать клетку мертвой']
