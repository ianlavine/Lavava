
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

LENGTH_FACTOR = 1.5
TRIANGLE_SIZE = 5
TRIANGLE_SPACING = 9
CIRCLE_RADIUS = 3
CIRCLE_SPACING = 6
EDGE_HIGHLIGHT_SPACING = 9

PORT_COUNT = 3

MINIMUM_TRANSFER_VALUE = 8

EDGE_CODE = 2
STANDARD_LEFT_CLICK = 1
STANDARD_RIGHT_CLICK = 3
CANNON_SHOT_CODE = 4
EDGE_ON = STANDARD_LEFT_CLICK
EDGE_SWAP = STANDARD_RIGHT_CLICK

ELIMINATE_VAL = -1
RESTART_GAME_VAL = -2
ABILITIES_SELECTED = -3

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

RESOURCE_BUBBLE = 400
ISLAND_RESOURCE_BUBBLE = 400

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
DARK_PINK = (255, 0, 127)
LIGHT_BLUE = (173, 216, 230)
BROWN = (150, 75, 0)
DARK_GRAY = (64, 64, 64)

RAGE_TICKS = 200
BURN_TICKS = 30

GROWTH_STOP = 250

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
CANNON_COST = 400

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
CANNON_CREDITS = 3

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
CANNON_RELOAD = 30

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
CANNON_CODE = 101

DEFAULT_ABILITY_CODE = SPAWN_CODE
RESTART_CODE = 32
FORFEIT_CODE = 120
OVERRIDE_RESTART_CODE = 121

ABILITY_CODES = {
    SPAWN_CODE,
    FREEZE_CODE,
    BURN_CODE,
    ZOMBIE_CODE,
    BRIDGE_CODE,
    D_BRIDGE_CODE,
    RAGE_CODE,
    POISON_CODE,
    NUKE_CODE,
    CAPITAL_CODE,
}

EVENT_CODES ={
    CANNON_SHOT_CODE,
    STANDARD_LEFT_CLICK,
    STANDARD_RIGHT_CLICK
}