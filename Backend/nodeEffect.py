from constants import (
    BURN_SPREAD_DELAY,
    BURN_TICKS,
    RAGE_TICKS,
    OVER_GROW_TICKS,
    RAGE_MULTIPLIER,
    POISON_SPREAD_DELAY,
    ZOMBIE_TICKS,
)
from effectEnums import EffectType
from abstractEffect import AbstractSpreadingEffect

class Poisoned(AbstractSpreadingEffect):
    def __init__(self, originator, length):
        super().__init__(length, EffectType.GROW, POISON_SPREAD_DELAY)
        self.originator = originator
       
    def can_spread(self, killed, new_owner):
        return self.originator != new_owner

    def effect(self, amount):
        return amount * -1
    
    def spread(self):
        return (self.originator, self.length - self.counter)
    
    def capture_removal(self, player) -> bool:
        return self.originator != player


class Enraged(AbstractSpreadingEffect):
    def __init__(self):
        super().__init__(RAGE_TICKS, EffectType.EXPEL)

    def effect(self, amount):
        return amount * RAGE_MULTIPLIER
    
    def can_spread(self, killed, new_owner):
        return killed
    
    def capture_removal(self, player):
        return False
    

class Zombified(AbstractSpreadingEffect):
    def __init__(self):
        super().__init__(ZOMBIE_TICKS, EffectType.INTAKE)
    
    def can_spread(self, killed, new_owner):
        return killed
    
    def capture_removal(self, player):
        return False
    
    def effect(self, amount):
        return amount * -2
    
    def spread_key(self, key):
        return "zombie"


class OverGrown(AbstractSpreadingEffect):
    def __init__(self):
        super().__init__(OVER_GROW_TICKS, EffectType.GROW)
    
    def effect(self, amount):
        return amount * 5
    
    def can_spread(self, killed, new_owner):
        return killed and new_owner.state_name == "default"

    def capture_removal(self, player):
        return False
    

class Burning(AbstractSpreadingEffect):
    def __init__(self):
        super().__init__(BURN_TICKS, EffectType.NONE, BURN_SPREAD_DELAY)
    
    def effect(self, amount):
        return 0

    def can_spread(self, killed, new_owner):
        return True

    def capture_removal(self, player):
        return True
