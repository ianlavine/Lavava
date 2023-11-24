from constants import GROWTH_RATE, MINIMUM_TRANSFER_VALUE, \
    CAPITAL_SHRINK_SPEED, MINE_DICT, GROWTH_STOP, GREY, TRANSFER_RATE, CONTEXT, GROWTH_STOP
from abc import ABC, abstractmethod
import math


class AbstractState(ABC):

    def __init__(self, id, kill_over):
        self.id = id
        self.kill_over = kill_over
        self.acceptBridge = True
        self.reset_on_capture = False

    def grow(self, multiplier):
        return GROWTH_RATE * multiplier

    @abstractmethod
    def intake(self, amount, multiplier, contested):
        pass

    def accept_intake(self, contested, value):
        return value < self.full_size

    def expel(self, multiplier):
        return TRANSFER_RATE * multiplier

    @abstractmethod
    def capture_event(self):
        pass

    def state_over(self, value):
        if self.kill_over:
            return self.killed(value)
        return False

    @abstractmethod
    def killed(self, value):
        pass

    def size_factor(self, value):
        if value<5:
            return 0
        return max(math.log10(value/10)/2+value/1000+0.15,0)

    @property
    def full_size(self):
        return GROWTH_STOP


class DefaultState(AbstractState):

    def __init__(self, id):
        super().__init__(id, False)

    def intake(self, amount, multiplier, contested):
        change = amount * multiplier
        if contested:
            change *= -1
        return change

    def capture_event(self):
        return -1

    def killed(self, value):
        return value < 0


class CapitalState(DefaultState):

    def __init__(self, id):
        super().__init__(id, True)
        self.capitalized = False
        self.acceptBridge = False
        self.shrink_count = math.ceil((GROWTH_STOP - MINIMUM_TRANSFER_VALUE) / abs(CAPITAL_SHRINK_SPEED))
        self.reset_on_capture = True

    def grow(self, multiplier):
        if not self.capitalized:
            return self.shrink()
        return 0

    def shrink(self):
        if self.shrink_count == 0:
            self.capitalized = True
            CONTEXT['main_player'].capital_handover(self)
            return 0
        self.shrink_count -= 1
        return CAPITAL_SHRINK_SPEED

    def capture_event(self):
        CONTEXT['main_player'].capital_handover(self, False)
        return super().capture_event()


class StartingCapitalState(CapitalState):

    def __init__(self, id, capital_handover, is_owned=True):
        super().__init__(id, capital_handover)
        self.capitalized = True
        self.is_owned = is_owned

    def grow(self, multiplier):
        return 0

    def capture_event(self):
        if self.is_owned:
            self.capital_handover(self, False)
        return DefaultState.capture(self)


class MineState(AbstractState):

    def __init__(self, id, absorbing_func, island):
        super().__init__(id, False)
        self.bonus, self.bubble, self.ring_color = MINE_DICT[island]
        self.absorbing_func = absorbing_func

    def grow(self, multipler):
        return 0

    def intake(self, amount, multiplier, contested):
        return amount * multiplier

    def accept_intake(self, contested, value):
        return not contested or self.absorbing_func()

    def killed(self, value):
        return False

    def state_over(self, value):
        return value >= self.bubble

    def capture_event(self):
        CONTEXT['main_player'].change_tick(self.bonus)
        return MINIMUM_TRANSFER_VALUE

    def size_factor(self, value):
        return super().size_factor(self.bubble)/2