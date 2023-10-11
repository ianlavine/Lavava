SERVER_K = '50.64.20.3'
# DEFAULT_SERVER = '192.168.2.19'
DEFAULT_SERVER_E = '192.168.1.106'

SERVER_FH = '192.168.9.109'
SERVER_I = '10.0.0.117'
SERVER_GD = '100.67.30.86'
SERVER_UG = '100.67.28.206'
SERVER_CO = '192.168.9.150'
SERVERS = {'k': SERVER_K, 'f': SERVER_FH, 'i': SERVER_I, 'g': SERVER_GD, 'u': SERVER_UG, 'c': SERVER_CO, 'e': DEFAULT_SERVER_E}

NODE_COUNT = 65
EDGE_COUNT = 60
MAX_EDGE_LENGTH = 7
ONE_WAY_COUNT = 17 # to 1
MIN_ANGLE = 15

NODE = 'node'
EDGE = 'edge'

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
size = (SCREEN_WIDTH, SCREEN_HEIGHT)

AUTO_EXPAND = True
AUTO_ATTACK = False

ABILITY_START_HEIGHT = 0.012
ABILITY_SIZE = 0.16
ABILITY_GAP = 0.165
ABILITY_FONT = 0.04
FONT_GAP = 0.028

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
ORANGE = (243, 156, 18)
YELLOW = (255, 255, 0)
DARK_YELLOW = (204, 204, 0)
GREY = (128, 128, 128)
LIGHT_GREY = (192, 192, 192)
PURPLE = (153, 51, 255)
PINK = (255, 51, 153)
LIGHT_BLUE = (173, 216, 230)

COLOR_DICT = {0: (RED, "   RED "), 1: (BLUE, "  BLUE "), 2: (ORANGE, "ORANGE "), 3: (GREEN, " GREEN ")}

GROWTH_RATE = 0.15
GROWTH_STOP = 250

TRANSFER_RATE = 0.02
MINIMUM_TRANSFER_VALUE = 8
BEGIN_TRANSFER_VALUE = 15

START_MONEY = 100
START_MONEY_RATE = 0.7

RESOURCE_BONUS = 0.2
RESOURCE_BUBBLE = 400
ISLAND_RESOURCE_BONUS = 0.4
ISLAND_RESOURCE_BUBBLE = 400
NETWORK_RESOURCE_COUNT = 3
ISLAND_RESOURCE_COUNT = 4
RESOURCE_RECOUP = 0.15

TICK = 0
ELIMINATE_VAL = -1
RESTART_GAME_VAL = -2

STANDARD_LEFT_CLICK = 1
STANDARD_RIGHT_CLICK = 3

SPAWN_COST = 100
SPAWN_CODE = 2

BRIDGE_CODE = 97
BRIDGE_COST = 200

NUKE_CODE = 110
NUKE_COST = 350

POISON_CODE = 112
POISON_COST = 400
POISON_TICKS = 500
POISON_SPREAD_DELAY = 3

DEFAULT_ABILITY_CODE = SPAWN_CODE

FREEZE_CODE = 102
FREEZE_COST = 50

CAPITAL_COST = 500
CAPITAL_CODE = 99
CAPITAL_BONUS = 0.2
CAPITAL_WIN_COUNT = 3
CAPITAL_SHRINK_SPEED = 20

ABILITY_CODES = {BRIDGE_CODE, NUKE_CODE, POISON_CODE, FREEZE_CODE, CAPITAL_CODE, SPAWN_CODE}

