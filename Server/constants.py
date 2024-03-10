from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class AbilityBreakdown:
    letter: str
    name: str
    cost: int
    reload: Optional[int] = None
    credits: Optional[int] = None
    tick: Optional[int] = None
    eliminate_val: Optional[int] = None

@dataclass
class AbilityVisual:
    ab: AbilityBreakdown
    shape: str
    color: tuple
    count: int = 0

CONTEXT = {}

NODE_COUNT = 65
EDGE_COUNT = 60
MAX_EDGE_LENGTH = 7
ONE_WAY_COUNT = 17  # to 1
MIN_ANGLE = 15

NODE = "node"
PORT_NODE = "port node"
EDGE = 'edge'
DYNAMIC_EDGE = 'dynamic edge'

MODES = {1: "Money", 2: "Reload", 3: "Ports"}

STATE_NAMES = {"default", "capital", "mine", "zombie"}
EFFECT_NAMES = {"burn", "poison", "rage"}

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

AUTO_EXPAND = True
AUTO_ATTACK = False

ABILITY_START_HEIGHT = 0.005
ABILITY_SIZE = 0.19
HORIZONTAL_ABILITY_GAP = 0.2
VERTICAL_ABILITY_GAP = 0.2
ABILITY_FONT = 0.05
FONT_GAP = 0.035

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
MEDIUM_GREEN = (179, 255, 149)
LIGHT_GREEN = (209, 255, 189)
DARK_GREEN = (0, 100, 0)
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
DARK_GRAY = (64, 64, 64)

COLOR_DICT = {
    0: (RED, "   RED "),
    1: (BLUE, "  BLUE "),
    2: (ORANGE, "ORANGE "),
    3: (GREEN, " GREEN "),
    4: (YELLOW, "YELLOW "),
}

GROWTH_RATE = 0.15
GROWTH_STOP = 250
ZOMBIE_FULL_SIZE = 200

TRANSFER_RATE = 0.02
MINIMUM_TRANSFER_VALUE = 8
BEGIN_TRANSFER_VALUE = 15

STANDARD_SWAP_STATUS = 1
BELOW_SWAP_STATUS = 0

START_MONEY = 0
START_MONEY_RATE = 0.7
START_CREDITS = 16

RESOURCE_BONUS = 0.2
RESOURCE_BUBBLE = 400
ISLAND_RESOURCE_BONUS = 0.4
ISLAND_RESOURCE_BUBBLE = 400
NETWORK_RESOURCE_COUNT = 3
ISLAND_RESOURCE_COUNT = 4
RESOURCE_RECOUP = 0.15

CAPITAL_START_COUNT = 2
CAPITAL_ISLAND_COUNT = 1

PORT_LAYOUT = [0, 2, 2]

MINE_DICT = {
    True: (ISLAND_RESOURCE_BONUS, ISLAND_RESOURCE_BUBBLE, YELLOW),
    False: (RESOURCE_BONUS, RESOURCE_BUBBLE, DARK_YELLOW),
}

TICK = 0
ELIMINATE_VAL = -1
RESTART_GAME_VAL = -2
ABILITIES_CHOSEN_VAL = -3

STANDARD_LEFT_CLICK = 1
STANDARD_RIGHT_CLICK = 3

BURN_TICKS = 30
POISON_TICKS = 500
RAGE_TICKS = 200

SPAWN_COST = 100
FREEZE_COST = 75
BURN_COST = 75
ZOMBIE_COST = 75
BRIDGE_COST = 175
D_BRIDGE_COST = 200
RAGE_COST = 100
NUKE_COST = 350
POISON_COST = 350
CAPITAL_COST = 450

SPAWN_CREDITS = 1
FREEZE_CREDITS = 1
BURN_CREDITS = 1
ZOMBIE_CREDITS = 1
BRIDGE_CREDITS = 2
D_BRIDGE_CREDITS = 2
RAGE_CREDITS = 2
POISON_CREDITS = 2
NUKE_CREDITS = 3
CAPITAL_CREDITS = 3

SPAWN_RELOAD = 30
FREEZE_RELOAD = 8
BURN_RELOAD = 5
ZOMBIE_RELOAD = 2
BRIDGE_RELOAD = 2
D_BRIDGE_RELOAD = 8
RAGE_RELOAD = int(RAGE_TICKS / 10)
NUKE_RELOAD = 20
POISON_RELOAD = 5
CAPITAL_RELOAD = 20

SPAWN_CODE = 115
FREEZE_CODE = 102
BRIDGE_CODE = 97
D_BRIDGE_CODE = 100
ZOMBIE_CODE = 122
RAGE_CODE = 114
BURN_CODE = 98
NUKE_CODE = 110
POISON_CODE = 112
CAPITAL_CODE = 99

POISON_SPREAD_DELAY = 5

DEFAULT_ABILITY_CODE = SPAWN_CODE
RESTART_CODE = 114
FORFEIT_CODE = 120
OVERRIDE_RESTART_CODE = 121

CAPITAL_BONUS = 0.2
CAPITAL_WIN_COUNT = 3
CAPITAL_SHRINK_SPEED = -20

RAGE_MULTIPLIER = 2.5

DEFAULT_ABILITY_CODE = SPAWN_CODE
RESTART_CODE = 114
FORFEIT_CODE = 120
OVERRIDE_RESTART_CODE = 121


LETTER_TO_CODE = {
    "S": SPAWN_CODE,
    "B": BURN_CODE,
    "A": BRIDGE_CODE,
    "D": D_BRIDGE_CODE,
    "P": POISON_CODE,
    "F": FREEZE_CODE,
    "N": NUKE_CODE,
    "C": CAPITAL_CODE,
    "R": RAGE_CODE,
    "Z": ZOMBIE_CODE,
}

ALL_ABILITIES = {
    SPAWN_CODE,
    BRIDGE_CODE,
    D_BRIDGE_CODE,
    NUKE_CODE,
    POISON_CODE,
    FREEZE_CODE,
    CAPITAL_CODE,
    BURN_CODE,
    RAGE_CODE,
    ZOMBIE_CODE,
}

SPAWN_BREAKDOWN = AbilityBreakdown("S", "Spawn", SPAWN_COST, SPAWN_RELOAD, SPAWN_CREDITS)
BRIDGE_BREAKDOWN = AbilityBreakdown("A", "Bridge", BRIDGE_COST, BRIDGE_RELOAD, BRIDGE_CREDITS)
D_BRIDGE_BREAKDOWN = AbilityBreakdown("D", "D-Bridge", D_BRIDGE_COST, D_BRIDGE_RELOAD, D_BRIDGE_CREDITS)
NUKE_BREAKDOWN = AbilityBreakdown("N", "Nuke", NUKE_COST, NUKE_RELOAD, NUKE_CREDITS)
POISON_BREAKDOWN = AbilityBreakdown("P", "Poison", POISON_COST, POISON_RELOAD, POISON_CREDITS)
FREEZE_BREAKDOWN = AbilityBreakdown("F", "Freeze", FREEZE_COST, FREEZE_RELOAD, FREEZE_CREDITS)
CAPITAL_BREAKDOWN = AbilityBreakdown("C", "Capital", CAPITAL_COST, CAPITAL_RELOAD, CAPITAL_CREDITS)
ZOMBIE_BREAKDOWN = AbilityBreakdown("Z", "Zombie", ZOMBIE_COST, ZOMBIE_RELOAD, ZOMBIE_CREDITS)
BURN_BREAKDOWN = AbilityBreakdown("B", "Burn", BURN_COST, BURN_RELOAD, BURN_CREDITS)
RAGE_BREAKDOWN = AbilityBreakdown("R", "Rage", RAGE_COST, RAGE_RELOAD, RAGE_CREDITS)

SPAWN_VISUAL = AbilityVisual(SPAWN_BREAKDOWN, "circle", (None,))
BRIDGE_VISUAL = AbilityVisual(BRIDGE_BREAKDOWN, "triangle", YELLOW)
D_BRIDGE_VISUAL = AbilityVisual(D_BRIDGE_BREAKDOWN, "circle", YELLOW)
NUKE_VISUAL = AbilityVisual(NUKE_BREAKDOWN, "x", BLACK)
POISON_VISUAL = AbilityVisual(POISON_BREAKDOWN,  "circle", PURPLE)
FREEZE_VISUAL = AbilityVisual(FREEZE_BREAKDOWN, "triangle", LIGHT_BLUE)
CAPITAL_VISUAL = AbilityVisual(CAPITAL_BREAKDOWN, "star", PINK)
ZOMBIE_VISUAL = AbilityVisual(ZOMBIE_BREAKDOWN, "square", (None,))
BURN_VISUAL = AbilityVisual(BURN_BREAKDOWN, "square", DARK_ORANGE)
RAGE_VISUAL = AbilityVisual(RAGE_BREAKDOWN,  "cross", GREEN)


BREAKDOWNS = {
    SPAWN_CODE: SPAWN_BREAKDOWN,
    FREEZE_CODE: FREEZE_BREAKDOWN,
    BURN_CODE: BURN_BREAKDOWN,
    ZOMBIE_CODE: ZOMBIE_BREAKDOWN,
    BRIDGE_CODE: BRIDGE_BREAKDOWN,
    D_BRIDGE_CODE: D_BRIDGE_BREAKDOWN,
    RAGE_CODE: RAGE_BREAKDOWN,
    POISON_CODE: POISON_BREAKDOWN,
    NUKE_CODE: NUKE_BREAKDOWN,
    CAPITAL_CODE: CAPITAL_BREAKDOWN,
}

VISUALS = {
    SPAWN_CODE: SPAWN_VISUAL,
    FREEZE_CODE: FREEZE_VISUAL,
    BURN_CODE: BURN_VISUAL,
    ZOMBIE_CODE: ZOMBIE_VISUAL,
    BRIDGE_CODE: BRIDGE_VISUAL,
    D_BRIDGE_CODE: D_BRIDGE_VISUAL,
    RAGE_CODE: RAGE_VISUAL,
    POISON_CODE: POISON_VISUAL,
    NUKE_CODE: NUKE_VISUAL,
    CAPITAL_CODE: CAPITAL_VISUAL,
    
}
