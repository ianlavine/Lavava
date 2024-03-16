from constants import (
    BURN_TICKS,
    POISON_TICKS,
    RAGE_TICKS,
    RAGE_MULTIPLIER,
    POISON_SPREAD_DELAY,
)
from effectEnums import EffectType
from abstractEffect import AbstractNodeEffect
from effect_spreaders import no_spread, single_spread, standard_outFlowing_sameOwner

class Burning(AbstractNodeEffect):
    def __init__(self, lose_ports):
        super().__init__(False, BURN_TICKS, EffectType.NONE, no_spread)
        self.lose_ports_func = lose_ports

    def complete(self):
        self.lose_ports_func()


class Poisoned(AbstractNodeEffect):
    def __init__(self, spread_poison):
        super().__init__(True, POISON_TICKS, EffectType.GROW, single_spread(POISON_SPREAD_DELAY), standard_outFlowing_sameOwner)
        self.spread_poison = spread_poison
 
    def effect(self, amount):
        return amount * -1

    def count(self):
        if self.counter == POISON_SPREAD_DELAY:
            self.spread_poison()
        return super().count()
        


class NodeEnraged(AbstractNodeEffect):
    def __init__(self):
        super().__init__(True, RAGE_TICKS, EffectType.EXPEL, no_spread)

    def effect(self, amount):
        return amount * RAGE_MULTIPLIER
