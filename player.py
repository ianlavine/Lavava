from constants import *

class DefaultPlayer:

    def __init__(self, color, id):
        self.default_color = color[0]
        self.name = color[1]
        self.id = id
        self.points = 0
        self.rage_count = 0
        self.default_values()

    def enrage(self):
        self.rage_count = RAGE_TICKS

    @property
    def raged(self):
        return self.rage_count > 0

    def default_values(self):
        self.count = 0
        self.begun = False
        self.eliminated = False
        self.victory = False
        self.color = self.default_color
        self.capitals = {}

    def eliminate(self):
        self.eliminated = True
        self.color = GREY
        self.points += self.count

    def update(self):
        if self.raged:
            self.rage_count -= 1

    def win(self):
        self.victory = True
        self.points += NODE_COUNT

    def display(self):
        print(f"{self.name}|| {self.points}")

    def capital_handover(self, capital, gain=True):
        if gain:
            self.capitals[capital.node.id] = capital
        else:
            del self.capitals[capital.node.id]
        
    def check_capital_win(self):
        return self.capital_count == CAPITAL_WIN_COUNT

    @property
    def capital_count(self):
        return len([c for c in self.capitals.values() if c.full])


class MoneyPlayer(DefaultPlayer):

    def default_values(self):
        self.money = START_MONEY
        self.tick_production = START_MONEY_RATE
        super().default_values()

    def change_tick(self, amount):
        self.tick_production += amount

    def capital_handover(self, capital, gain=True):
        if gain:
            self.tick_production += CAPITAL_BONUS
        else:
            self.tick_production -= CAPITAL_BONUS
        super().capital_handover(capital, gain)

    def eliminate(self):
        self.money = 0
        super().eliminate()

    def update(self):
        self.money += self.tick_production
        super().update()

    @property
    def production_per_second(self):
        return self.tick_production * 10

    
