from abc import ABC, abstractmethod

class AbstractEffect(ABC):

    def __init__(self, expiry_time):
        self.length = expiry_time
        self.counter = expiry_time

    def count(self):
        self.counter -= 1
        return self.counter > 0 

    def complete(self):
        pass


class AbstractNodeEffect(AbstractEffect):

    def __init__(self, reset_on_capture, expiry_time, effect_type, can_spread, spread_criteria=None):
        super().__init__(expiry_time)
        self.reset_on_capture = reset_on_capture
        self.effect_type = effect_type
        self.can_spread_func = can_spread
        self.spread_criteria_func = spread_criteria


class AbstractPlayerEffect(AbstractEffect):

    @abstractmethod
    def spread(self, node):
        pass