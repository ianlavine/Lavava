from powerBox import PowerBox
from constants import *

def make_boxes():
    return {
        BRIDGE_CODE: PowerBox('Bridge', YELLOW, 'triangle', 'A'),
        POISON_CODE: PowerBox('Poison', PURPLE, 'circle'),
        FREEZE_CODE: PowerBox('Freeze', LIGHT_BLUE, 'triangle'),
        BURN_CODE: PowerBox('Burn', DARK_ORANGE, 'square'),
        D_BRIDGE_CODE: PowerBox('D-Bridge', YELLOW, 'circle'),
        NUKE_CODE: PowerBox('Nuke', BLACK, 'square'),
        CAPITAL_CODE: PowerBox('Capital', PINK, 'star'),
        RAGE_CODE: PowerBox('Rage', GREEN, 'star'),
        SPAWN_CODE: PowerBox('Spawn', CONTEXT['main_player'].default_color, 'circle', ''),
    }