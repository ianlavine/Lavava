from abc import ABC, abstractmethod

class AbstractEffect(ABC):

    def __init__(self, expiry_time, effect_type):
        self.length = expiry_time
        self.effect_type = effect_type
        self.counter = 0

    def count(self):
        self.counter += 1
        return self.counter < self.length
    
    @abstractmethod
    def effect(self, amount) -> float:
        pass

class AbstractSpreadingEffect(AbstractEffect):

    def __init__(self, expiry_time, effect_type, back_spread, incubation_timer=0):
        super().__init__(expiry_time, effect_type)
        self.back_spread = back_spread
        self.incubation_timer = incubation_timer

    @property
    def past_incubation(self):
        return self.counter > self.incubation_timer

    @abstractmethod
    def can_spread(self, killed, new_owner) -> bool:
        pass

    @abstractmethod
    def capture_removal(self, player) -> bool:
        pass

    def spread(self):
        return None
    
    def spread_key(self, key):
        return key