import os

MENU = 0
GAME = 1
SETTINGS = 2

MAX_SPEED = 12
ACCELERATION = 0.5

GAME_DURATION = 120

ASSETS = os.path.abspath(os.path.join(os.path.dirname(__file__), 'assets'))
BACKGROUND_FOLDER = os.path.join(ASSETS, 'backgrounds')
PLAYER_FOLDER = os.path.join(ASSETS, 'players')

DARK = (31, 32, 65)
LIGHT_DARK = (62, 64, 130)

