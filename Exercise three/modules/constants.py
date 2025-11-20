"""
Constants for Student Manager
"""
import os

# Window
WIDTH = 1200
HEIGHT = 675

# Files - PROPER OS PATHS
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "media", "studentMarks.txt")
BG_IMAGE = os.path.join(BASE_DIR, "media", "student_manager_bg.jpg")

# start screen buttons
START_BTN_WIDTH = 1000
START_BTN_HEIGHT = 500
START_BTN_Y = 400
QUIT_BTN_WIDTH = 600
QUIT_BTN_HEIGHT = 300
QUIT_BTN_X = WIDTH - 60
QUIT_BTN_Y = 100

# Tutorial assets
TUTORIAL_1 = os.path.join(BASE_DIR, "media", "tutorial_1.png")
TUTORIAL_2 = os.path.join(BASE_DIR, "media", "tutorial_2.png")

# Tutorial button colors
TUTORIAL_NEXT_COLOR = 'green'
TUTORIAL_SKIP_COLOR = 'red'
TUTORIAL_BUTTON_TEXT_COLOR = 'white'

# start screen assets
START_BG = os.path.join(BASE_DIR, "media", "main_bg.png")
START_BUTTON = os.path.join(BASE_DIR, "media", "start.png")
QUIT_BUTTON = os.path.join(BASE_DIR, "media", "quit.png")

# positions
POSITIONS = [110, 300, 500, 705, 895, 1095]

COLORS = {
    'title': '#fc84ff',
    'content': '#fff8db',
    'button': '#c0c0c0',
    'hover': '#a0a0a0',
    'success': '#27AE60',
    'danger': '#C0392B'
}

FONT = 'Comic Sans MS'
FONT_SIZES = {
    'title': 24,
    'stats_label': 17,
    'stats_value': 15,
    'button': 18,
    'header': 12,
    'cell': 10,
    'detail_label': 14,
    'detail_value': 12,
    'form': 12
}

POS = {
    'title_y': 40,
    'stats_y': 110,
    'buttons_y': 182,
    'list_x': 400,
    'list_y': 415,
    'list_w': 710,
    'list_h': 320,
    'details_x': 980,
    'details_y': 430,
    'details_w': 350,
    'details_h': 350
}
TABLE = {
    'headers': ["ID", "Name", "CW1", "CW2", "CW3", "CW Total", "Exam", "Total", "Grade"],
    'col_w': 12,
    'select_color': '#a0c8f0'
}