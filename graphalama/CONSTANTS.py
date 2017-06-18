# -*- coding: utf-8 -*-
# some control messages
ok = 'ok !'
yay = 'yay !'
yayy = 'yay !!!!!!!!!'
test = 'test....'

# some colors
BLACK = (0, 0, 0)
GREY_90 = (25, 25, 25)
GREY_75 = (64, 64, 64)
GREY_50 = (128, 128, 128)
GREY_25 = (182, 182, 182)
GREY_10 = (220, 220, 200)
WHITE = (255, 255, 255)

TRANSPARENT = (255, 255, 255, 0)

GREY_BLUE = (128, 128, 180)

DARK_RED = (200, 0, 0)
DARK_GREEN = (0, 200, 0)

RED = (255, 0, 0)
ORANGE = (255, 128, 0)
YELLOW = (255, 255, 0)
LIGHT_GREEN = (128, 255, 0)
GREEN = (0, 255, 0)
BLEEN = (0, 255, 128)
CYAN = (0, 255, 255)
LIGHT_BLUE = (0, 128, 255)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 255)
MAGENTA = (255, 0, 255)
PINK = (255, 0, 128)

L_RED = (255, 60, 60)
L_ORANGE = (255, 168, 70)
L_YELLOW = (255, 255, 130)
L_LIGHT_GREEN = (158, 255, 70)
L_GREEN = (80, 255, 80)
L_BLEEN = (90, 255, 158)
L_CYAN = (90, 210, 255)
L_LIGHT_BLUE = (70, 158, 255)
L_BLUE = (50, 70, 255)
L_PURPLE = (178, 90, 255)
L_MAGENTA = (255, 140, 255)
L_PINK = (255, 70, 158)

# numbers
PHI = 1.61803398875

# special constants
RECTANGLE = 85
ROUNDED = 81
PROPORTION = 'P'
DIVIDE = '/'
MULTIPLY = '*'
NO = '__none__'
NOCOPY = '__nocopy__'
DEEPCOPY = '__deepcopy__'

# Text's options
ONELINE = '__oneline__'
ADAPT_L = '__adapt_l__'
FILL_SPACE = '__fill_space__'
SIZE_MIN_LEFT = '__size_min_left__'
SIZE_MIN_RIGHT = '__size_min_right__'
SIZE_MIN_DOWN = '__size_min_down__'
SIZE_MIN_UP = '__size_min_up__'

# TextBox's options
NO_CURSOR = '__no_cursor__'

# Priorities, sizes
NOTHING = '__nothing__'
ALL = '__all__'
SMALL = '__small__'
BIG = '__big__'
NEXT = '__next__'
END_OF_FRAME = '__end_of_frame__'

# Click controls options
JUST_PRESSED = 'just pressed'
IS_PRESSED = 'is pressed'

# some color lists
BRIGHT_COLORS = [WHITE, RED, ORANGE, YELLOW, LIGHT_GREEN, GREEN, BLEEN, CYAN, LIGHT_BLUE, BLUE, PURPLE, MAGENTA, PINK]
L_BRIGHT_COLORS = [GREY_25, L_RED, L_ORANGE, L_YELLOW, L_LIGHT_GREEN, L_GREEN, L_BLEEN, L_CYAN, L_LIGHT_BLUE, L_BLUE,
                   L_PURPLE, L_MAGENTA, L_PINK]
GREYS = [WHITE, GREY_10, GREY_25, GREY_50, GREY_75, GREY_90, BLACK]

# some color dicts
D_BRIGHT_COLORS = dict()
for i, c in enumerate(BRIGHT_COLORS):
    D_BRIGHT_COLORS[str(i)] = c

D_L_BRIGHT_COLORS = dict()
for i, c in enumerate(L_BRIGHT_COLORS):
    D_L_BRIGHT_COLORS[str(i)] = c

# noinspection PyUnboundLocalVariable
del c, i
