from constants import (
    GREY,
    NODE_COUNT,
    CAPITAL_WIN_COUNT,
    START_MONEY,
    START_MONEY_RATE,
    CAPITAL_BONUS,
)


class DefaultPlayer:
    def __init__(self, color, id):
        self.default_color = color[0]
        self.name = color[1]
        self.id = id
        self.points = 0
        self.effects = set()
        self.default_values()

    def default_values(self):
        self.count = 0
        self.begun = False
        self.eliminated = False
        self.victory = False
        self.color = self.default_color
        self.full_capital_count = 0

    def eliminate(self):
        self.eliminated = True
        self.color = GREY
        self.points += self.count

    def update(self):
        self.effects = set(filter(lambda effect : (effect.count()), self.effects))

    def pass_on_effects(self, node):
        for effect in self.effects:
            effect.spread(node)

    def win(self):
        self.victory = True
        self.points += NODE_COUNT

    def display(self):
        print(f"{self.name}|| {self.points}")

    def capital_handover(self, gain):
        pass

    def check_capital_win(self):
        return self.full_capital_count == CAPITAL_WIN_COUNT


class MoneyPlayer(DefaultPlayer):
    def default_values(self):
        self.money = START_MONEY
        self.tick_production = START_MONEY_RATE
        super().default_values()

    def change_tick(self, amount):
        self.tick_production += amount

    def capital_handover(self, gain):
        if gain:
            self.tick_production += CAPITAL_BONUS
        else:
            self.tick_production -= CAPITAL_BONUS
        super().capital_handover(gain)

    def eliminate(self):
        self.money = 0
        super().eliminate()

    def update(self):
        self.money += self.tick_production
        super().update()

    @property
    def production_per_second(self):
        return self.tick_production * 10
