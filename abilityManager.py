from constants import *
from abc import ABC, abstractmethod
from ability import *
from ability_factory import make_abilities
from chooseUI import choose_abilities_ui

class AbstractAbilityManager(ABC):
    def __init__(self, board):
        self.ability_codes = choose_abilities_ui()
        self.abilities = self.create_abilities(board)
        self.mode = DEFAULT_ABILITY_CODE

    def set_box_numbers(self, stat):
        for ability in self.abilities.values():
            ability.box.set_stat_func(lambda key=ability.key: stat[key])

    def create_abilities(self, board):
        codes = self.ability_codes
        all_dict = make_abilities(board)
        return {k: all_dict[k] for k in codes}

    def use_ability(self, item, color):
        if self.ability.click_type == item.type and self.box.color == color:
            return self.ability.complete(item)
        return False

    def switch_to(self, key):
        self.mode = key
        return self.ability.complete_check()

    def update(self):
        pass

    @abstractmethod
    def select(self, key):
        pass

    @abstractmethod
    def update_ability(self):
        pass

    @abstractmethod
    def default_validate(self):
        pass

    @property
    def ability(self):
        return self.abilities[self.mode]

    @property
    def box(self):
        return self.ability.box

class MoneyAbilityManager(AbstractAbilityManager):
    def __init__(self, board):
        super().__init__(board)
        self.costs = {code: BREAKDOWNS[code]['cost'] for code in self.ability_codes}
        self.set_box_numbers(self.costs)

    def select(self, key):
        self.abilities[self.mode].wipe()
        if self.mode == key:
            self.mode = DEFAULT_ABILITY_CODE
        elif CONTEXT['main_player'].money >= self.costs[key]:
            return self.switch_to(key)
        return False

    def update_ability(self):
        CONTEXT['main_player'].money -= self.costs[self.mode]
        if self.costs[self.mode] > CONTEXT['main_player'].money or self.mode == RAGE_CODE:
            self.mode = DEFAULT_ABILITY_CODE

    def default_validate(self):
        return CONTEXT['main_player'].money >= self.costs[SPAWN_CODE]

class ReloadAbilityManager(AbstractAbilityManager):
    def __init__(self, board):
        super().__init__(board)
        self.load_count = {code: 0 for code in self.ability_codes}
        self.load_count[SPAWN_CODE] = SPAWN_RELOAD
        self.remaining_usage = {code: BREAKDOWNS[code]['total'] for code in self.ability_codes}
        self.full_reload = {code: BREAKDOWNS[code]['reload'] for code in self.ability_codes}
        self.set_box_numbers(self.remaining_usage)

    def select(self, key):
        self.abilities[self.mode].wipe()
        if self.mode == key:
            self.mode = DEFAULT_ABILITY_CODE
        elif self.full(key):
            return self.switch_to(key)
        return False

    def update_ability(self):
        self.load_count[self.mode] = 0
        self.remaining_usage[self.mode] -= 1
        self.mode = DEFAULT_ABILITY_CODE

    def update(self):
        for key in self.load_count:
            if self.remaining_usage[key] > 0:
                if not self.full(key):
                    self.load_count[key] += 0.1

    def default_validate(self):
        return self.full(DEFAULT_ABILITY_CODE)

    def full(self, key):
        return self.load_count[key] >= self.full_reload[key]