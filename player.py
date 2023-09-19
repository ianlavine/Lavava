from constants import *
from math import sqrt

class Player:

    def __init__(self, color, id):
        self.count = 0
        self.color = color
        self.id = id
        self.auto_expand = True
        self.auto_attack = False
        self.new_edge_start = None
        self.highlighted_node = None
        self.eliminated = False
        self.victory = False
        self.started = False
        self.remaining_node_buys = RAW_START_NODES

    def buy_node(self):
        if self.remaining_node_buys > 0:
            self.started = True
            self.remaining_node_buys -= 1
            return True
        return False

    def eliminate(self):
        self.eliminated = True
        self.money = 0
        self.color = GREY

    def update(self):
        if not self.eliminated:
            return self.started and self.count == 0
        return False

    def win(self):
        self.victory = True