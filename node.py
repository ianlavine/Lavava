import math
from constants import *

class Node:

    def __init__(self, id, pos):
        self.value = 0
        self.owner = None
        self.clicker = None
        self.incoming = []
        self.outgoing = []
        self.id = id
        self.pos = pos
        self.popped = True

    def __str__(self):
        return str(self.id)

    def grow(self):
        if not self.full:
            self.value += GROWTH_RATE

    def click(self, clicker, button):
        self.clicker = clicker
        if button == 1:
            self.left_click(clicker)
        elif button == 3:
            self.right_click()

    def right_click(self):
        pass

    def left_click(self, clicker):
        if self.owner == None:
            if clicker.buy_node():
                self.capture()

    def delivery(self, amount, player):
        if self.owner != player:
            self.value -= amount
            if self.killed():
                self.capture(player)
        else:
            self.value += amount

    def attack(self):
        pass
        # self.absorb(True)

    def absorb(self, on):
        pass
        # for edge in self.incoming:
        #     if edge.owned_by(self.clicker):
        #         edge.switch(on)

    def expel(self, on):
        pass
        # for edge in self.outgoing:
        #     if not on or not edge.contested:
        #         edge.switch(on)

    def expand(self):
        for edge in self.outgoing:
            if edge.contested:
                if self.owner.auto_attack:
                    edge.switch(True)
                    edge.popped = True
            elif not edge.owned and self.owner.auto_expand:
                edge.switch(True)
                edge.popped = False

    def check_edge_stati(self):
        for edge in self.incoming:
            edge.check_status()
        for edge in self.outgoing:
            edge.check_status()

    def capture(self, clicker=None):
        if clicker is None:
            clicker = self.clicker
        self.owner = clicker
        clicker.count += 1
        self.check_edge_stati()
        self.expand()

    def killed(self):
        if self.value < 0:
            self.value *= -1
            if self.owner:
                self.owner.count -= 1
            return True
        return False

    def size_factor(self):
        if self.value<5:
            return 0
        return max(math.log10(self.value/10)/2+self.value/1000+0.15,0)

    @property
    def current_incoming(self):
        return [edge for edge in self.incoming if edge.to_node == self]

    @property
    def size(self):
        return int(5+self.size_factor()*18)

    @property
    def color(self):
        if self.owner:
            if self.value >= 250:
                return self.owner.color
            return self.owner.color
        return BLACK

    @property
    def full(self):
        return self.value >= GROWTH_STOP

    def set_pos_per(self):
        self.pos_x_per = self.pos[0] / SCREEN_WIDTH
        self.pos_y_per = self.pos[1] / SCREEN_HEIGHT

    def relocate(self, width, height):
        self.pos = (self.pos_x_per * width, self.pos_y_per * height)

    def owned_and_alive(self):
        return self.owner != None and not self.owner.eliminated
