NODE_COUNT = 65
EDGE_COUNT = 60
MAX_EDGE_LENGTH = 7
ONE_WAY_COUNT = 17 # to 1
MIN_ANGLE = 15

NODE = 'node'
PORT_NODE = 'port node'
EDGE = 3000
DYNAMIC_EDGE = 3500

MODES = {1: 'Money', 2: 'Reload', 3: 'Ports'}

STATE_NAMES = {'default', 'capital', 'mine'}
EFFECT_NAMES = {'burn', 'poison', 'rage'}

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
size = (SCREEN_WIDTH, SCREEN_HEIGHT)

AUTO_EXPAND = True
AUTO_ATTACK = False

ABILITY_START_HEIGHT = 0.005
ABILITY_SIZE = 0.19
ABILITY_GAP = 0.2
ABILITY_FONT = 0.05
FONT_GAP = 0.035

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
MEDIUM_GREEN = (179,255,149)
LIGHT_GREEN = (209,255,189)
ORANGE = (243, 156, 18)
DARK_ORANGE = (193, 106, 8)
STRONG_ORANGE = (255, 77, 0)
YELLOW = (255, 255, 0)
DARK_YELLOW = (204, 204, 0)
GREY = (128, 128, 128)
LIGHT_GREY = (192, 192, 192)
PURPLE = (153, 51, 255)
PINK = (255, 51, 153)
LIGHT_BLUE = (173, 216, 230)
BROWN = (150, 75, 0)

COLOR_DICT = {0: (RED, "   RED "), 1: (BLUE, "  BLUE "), 2: (ORANGE, "ORANGE "), 3: (GREEN, " GREEN "), 4: (YELLOW, "YELLOW ")}

GROWTH_RATE = 0.15
GROWTH_STOP = 250

TRANSFER_RATE = 0.02
MINIMUM_TRANSFER_VALUE = 8
BEGIN_TRANSFER_VALUE = 15

STANDARD_SWAP_STATUS = 1
BELOW_SWAP_STATUS = 0

START_MONEY = 100
START_MONEY_RATE = 0.7

RESOURCE_BONUS = 0.2
RESOURCE_BUBBLE = 400
ISLAND_RESOURCE_BONUS = 0.4
ISLAND_RESOURCE_BUBBLE = 400
NETWORK_RESOURCE_COUNT = 3
ISLAND_RESOURCE_COUNT = 4
RESOURCE_RECOUP = 0.15

CAPITAL_START_COUNT = 4
CAPITAL_ISLAND_COUNT = 1

PORT_LAYOUT = [0, 3]

MINE_DICT = {True: (ISLAND_RESOURCE_BONUS, ISLAND_RESOURCE_BUBBLE, YELLOW),
            False: (RESOURCE_BONUS, RESOURCE_BUBBLE, DARK_YELLOW)}

TICK = 0
ELIMINATE_VAL = -1
RESTART_GAME_VAL = -2
ABILITIES_CHOSEN_VAL = -3

STANDARD_LEFT_CLICK = 1
STANDARD_RIGHT_CLICK = 3

SPAWN_COST = 100
SPAWN_RELOAD = 200
SPAWN_TOTAL = 2
SPAWN_CODE = 2

BRIDGE_CODE = 97
BRIDGE_RELOAD = 15
BRIDGE_TOTAL = 4
BRIDGE_COST = 175

BURN_CODE = 98
BURN_COST = 125
BURN_TICKS = 30

D_BRIDGE_CODE = 100
D_BRIDGE_COST = 200
D_BRIDGE_RELOAD = 15
D_BRIDGE_TOTAL = 4

NUKE_CODE = 110
NUKE_COST = 350
NUKE_RELOAD = 15
NUKE_TOTAL = 3

POISON_CODE = 112
POISON_COST = 350
POISON_RELOAD = 15
POISON_TOTAL = 3
POISON_TICKS = 500
POISON_SPREAD_DELAY = 5

DEFAULT_ABILITY_CODE = SPAWN_CODE

FREEZE_CODE = 102
FREEZE_RELOAD = 10
FREEZE_TOTAL = 6
FREEZE_COST = 75

CAPITAL_COST = 450
CAPITAL_CODE = 99
CAPITAL_BONUS = 0.2
CAPITAL_WIN_COUNT = 3
CAPITAL_SHRINK_SPEED = -20

RAGE_COST = 100
RAGE_CODE = 114
RAGE_RELOAD = 10
RAGE_TOTAL = 4
RAGE_TICKS = 200
RAGE_MULTIPLIER = 2.5

LETTER_TO_CODE = {'S': SPAWN_CODE, 'B': BURN_CODE, 'A': BRIDGE_CODE, 'D': D_BRIDGE_CODE, 'P': POISON_CODE, 'F': FREEZE_CODE, 'N': NUKE_CODE, 'C': CAPITAL_CODE, 'R': RAGE_CODE}

RELOAD_ABILITIES = {BRIDGE_CODE, D_BRIDGE_CODE, NUKE_CODE, POISON_CODE, FREEZE_CODE, RAGE_CODE}
MONEY_ABILITIES = {BRIDGE_CODE, D_BRIDGE_CODE, NUKE_CODE, POISON_CODE, FREEZE_CODE, CAPITAL_CODE, RAGE_CODE}
PORTS_ABILITIES = {BRIDGE_CODE, D_BRIDGE_CODE, NUKE_CODE, POISON_CODE, FREEZE_CODE, CAPITAL_CODE, BURN_CODE, RAGE_CODE}
MODE_ABILITY_OPTIONS = {1: MONEY_ABILITIES, 2: RELOAD_ABILITIES, 3: PORTS_ABILITIES}

SPAWN_BREAKDOWN = {'letter': 'S', 'name': 'Spawn', 'cost': SPAWN_COST, 'reload': SPAWN_RELOAD, 'total': SPAWN_TOTAL}
BRIDGE_BREAKDOWN = {'letter': 'A', 'name': 'Bridge', 'cost': BRIDGE_COST, 'reload': BRIDGE_RELOAD, 'total': BRIDGE_TOTAL}
D_BRIDGE_BREAKDOWN = {'letter': 'D', 'name': 'D-Bridge', 'cost': D_BRIDGE_COST, 'reload': D_BRIDGE_RELOAD, 'total': D_BRIDGE_TOTAL}
NUKE_BREAKDOWN = {'letter': 'N', 'name': 'Nuke', 'cost': NUKE_COST, 'reload': NUKE_RELOAD, 'total': NUKE_TOTAL}
POISON_BREAKDOWN = {'letter': 'P', 'name': 'Poison', 'cost': POISON_COST, 'reload': POISON_RELOAD, 'total': POISON_TOTAL}
FREEZE_BREAKDOWN = {'letter': 'F', 'name': 'Freeze', 'cost': FREEZE_COST, 'reload': FREEZE_RELOAD, 'total': FREEZE_TOTAL}
CAPITAL_BREAKDOWN = {'letter': 'C', 'name': 'Capital', 'cost': CAPITAL_COST}
BURN_BREAKDOWN = {'letter': 'B', 'name': 'Burn', 'cost': BURN_COST}
RAGE_BREAKDOWN = {'letter': 'R', 'name': 'Rage', 'cost': RAGE_COST, 'reload': RAGE_RELOAD, 'total': RAGE_TOTAL}
BREAKDOWNS = {SPAWN_CODE: SPAWN_BREAKDOWN, BRIDGE_CODE: BRIDGE_BREAKDOWN,
            D_BRIDGE_CODE: D_BRIDGE_BREAKDOWN, NUKE_CODE: NUKE_BREAKDOWN,
            POISON_CODE: POISON_BREAKDOWN, FREEZE_CODE: FREEZE_BREAKDOWN,
            CAPITAL_CODE: CAPITAL_BREAKDOWN, BURN_CODE: BURN_BREAKDOWN,
            RAGE_CODE: RAGE_BREAKDOWN}