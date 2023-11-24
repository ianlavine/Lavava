from abc import ABC
from constants import BURN_TICKS, POISON_TICKS, RAGE_TICKS, RAGE_MULTIPLIER, POISON_SPREAD_DELAY
from effectEnums import EffectType

class AbstractEffect(ABC):

    def __init__(self, expiry_time, effect_type):
        self.expiry_time = expiry_time
        self.counter = 0
        self.effect_type = effect_type

    def count(self):
        self.counter += 1

    def complete(self):
        pass

    def effect(self, amount):
        return amount

    @property
    def expired(self):
        return self.counter >= self.expiry_time


class Burning(AbstractEffect):

    def __init__(self, lose_ports):
        super().__init__(BURN_TICKS, EffectType.NONE)
        self.lose_ports_func = lose_ports

    def complete(self):
        self.lose_ports_func()


class Poisoned(AbstractEffect):

    def __init__(self, spread_poison):
        super().__init__(POISON_TICKS, EffectType.GROW)

    def effect(self, amount):
        return amount * -1

    def count(self):
        if self.counter == POISON_SPREAD_DELAY:
            self.spread_poison()
        super().count()


class Enraged(AbstractEffect):

    def __init__(self):
        super().__init__(RAGE_TICKS, EffectType.EXPEL)

    def effect(self, amount):
        return amount * RAGE_MULTIPLIER
        