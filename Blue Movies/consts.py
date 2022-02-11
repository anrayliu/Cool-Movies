from win32api import GetSystemMetrics
import sky
from os import listdir, mkdir, rmdir, remove
from os.path import exists, join
from pickle import dump

WIN_W = GetSystemMetrics(0)
WIN_H = GetSystemMetrics(1)
WIN_SIZE = (WIN_W, WIN_H)
WIN_CENTER_X = round(WIN_W / 2)
WIN_CENTER_Y = round(WIN_H / 2)
WIN_MARG = round(WIN_W * 0.05)
P_FOLDER = "data"
P_TEMP = f"{P_FOLDER}\\temp"
P_WP = f"{P_FOLDER}\\wallpapers"
P_HTML = f"{P_TEMP}\\watch.html"
P_AVATARS = f"{P_FOLDER}\\avatars"
P_SAVE = f"{P_FOLDER}\\save.p"
P_CHANGELOG = f"{P_FOLDER}\\changelog.p"
REQUIRED_PATHS = ["add.png", "font.otf", "search.png", "star.png", "unknown.png", "user.png", "wallpaper.png", "arrow.png", "changelog.p", "log.png"]
VERSION = "1.0.1"
NAME = f"Blue Movies v{VERSION}"
WP_SPEED = 1/80
DISPLAY_ALPHA = 150
DISPLAY_X = WIN_MARG
DISPLAY_Y = WIN_MARG + 81 #81 represents font height rendered at 80 size
DISPLAY_W = round(WIN_W * 0.6)
DISPLAY_H = WIN_H - DISPLAY_Y - WIN_MARG
DISPLAY_MARG = round(DISPLAY_W * 0.05)
BUTTONS = ["Search", "Your list"]
BUTTON_MAX_ALPHA = 150
BUTTON_MIN_ALPHA = 5
ALPHA_ACCEL = 1.25
ALPHA_DEACCEL = 0.95
BUTTON_W = round(DISPLAY_W / len(BUTTONS))
BUTTON_H = 65 #tab nav buttons 
LOCATIONS_X = DISPLAY_X + DISPLAY_MARG  #where actual buttons and elements can start
LOCATIONS_Y = DISPLAY_Y + DISPLAY_MARG + BUTTON_H
LOCATIONS_W = DISPLAY_W - DISPLAY_MARG * 2
LOCATIONS_H = DISPLAY_H - DISPLAY_MARG * 2 - BUTTON_H
LOCATIONS_CENTER_X = round(DISPLAY_X + DISPLAY_W / 2)
LOCATIONS_CENTER_Y = round(DISPLAY_Y + BUTTON_H + (DISPLAY_H - BUTTON_H) / 2)
LOCATIONS_RECT = (LOCATIONS_X, LOCATIONS_Y, LOCATIONS_W, LOCATIONS_H)
SEARCH_H = 50
SEARCH_MIN_W = 100
SEARCH_MARG = 20
SEARCH_R = 20 #bar roundness
SB_R = 30 #search button
BACKSPACE_THRESHOLD = 25 #ticks until repeated backspacing
LC_R = 50 #loading circle radius
LC_ARC_SIZE = 60
LC_SPEED = 5
LC_COLOUR = sky.BLUE
SLIDER_W = 30
RESULTS_X = LOCATIONS_X
RESULTS_Y = LOCATIONS_Y + SEARCH_H + DISPLAY_MARG
RESULTS_W = LOCATIONS_W - SLIDER_W
RESULTS_H = LOCATIONS_H - DISPLAY_MARG - SEARCH_H
RESULTS_ALPHA = 100
INACTIVE_ALPHA = 128 #for buttons
IMG_RATIO = 2 / 3 #aspect ratio
IMG_W = round(LOCATIONS_W * 0.18)
IMG_H = round(IMG_W * IMG_RATIO ** -1)
IMG_LW = round(LOCATIONS_W * 0.3)
IMG_LH = round(IMG_LW * IMG_RATIO ** -1)
CARD_W = IMG_W
CARD_H = IMG_H + 40
CARD_COLUMNS = 4
MAX_RESULTS = CARD_COLUMNS * 3
CARD_SPACING_Y = 30
DD_W = 100 #dropdown
DD_H = SEARCH_H
DD_X = LOCATIONS_X + LOCATIONS_W - SB_R * 2 - DISPLAY_MARG - DD_W
DD_Y = LOCATIONS_Y
WHEEL_SENSITIVITY = 20
BB_W = 120 #back button
BB_H = 50
CARD_TITLE_LENGTH = 25
TITLE_LENGTH = 45 #for inspector and list
MAX_GENRES = 3
INFO_SPACING = 25 #spacing when iterating through info dict
INSPECTOR_BUTTONS_START = (LOCATIONS_X + IMG_LW + DISPLAY_MARG, LOCATIONS_Y + BB_H + DISPLAY_MARG * 2 + INFO_SPACING * 5)
INSPECTOR_BUTTON_W = round(DISPLAY_W * 0.25)
INSPECTOR_BUTTON_H = 50
INSPECTOR_BUTTON_SPACING = 20
LB_AMOUNT = 8 #list buttons per page
LB_H = round(LOCATIONS_H / LB_AMOUNT)
LIST_LAST_RECT_W = 50 #creates rects to center star and rating
LIST_BUTTON_MIN_ALPHA = 20
ACCOUNT_W = round(WIN_W * 0.15)
ACCOUNT_H = round(WIN_H * 0.3)
MAX_ACCOUNTS = 4
MAX_NAME_LENGTH = 20 #for accounts
RATING_STAR_SIZE = 50 
RATING_W = 100 #text box
RATING_H = 50
WATCHED_STAR_SIZE = 30
STAR_ALPHA = 150
KEY_CHANGE_WP = "right"
EB_W = 80 #enter button
EB_H = SEARCH_H
CHANGELOG_BORDER_SIZE = DISPLAY_MARG * 2 
CHANGELOG_INNER_ALPHA = 150
CHANGELOG_OUTER_ALPHA = 170
CHANGELOG_FONT_SIZE = 40
TRAY_B_SIZE = 60
TRAY_ALPHA = 200 
TRAY_HOVER_ALPHA = 100 
TRAY_W = 300 
TRAY_H = 200

if exists(P_TEMP):
    try:
        remove(P_HTML)
    except FileNotFoundError:
        pass
    rmdir(P_TEMP)
sky.confirm_assets([P_FOLDER])
[mkdir(dir) for dir in [P_AVATARS, P_WP, P_TEMP] if not exists(dir)]
if not exists(P_SAVE):
    with open(P_SAVE, "wb") as file:
        dump([[], [], True, VERSION], file)
sky.confirm_assets([join(P_FOLDER, path) for path in REQUIRED_PATHS])

WALLPAPERS = [file[:-4] for file in listdir(P_WP) if file[-4:] == ".jpg" or file[-4:] == ".png"]
AVATARS = [file[:-4] for file in listdir(P_AVATARS) if file[-4:] == ".jpg" or file[-4:] == ".png"]