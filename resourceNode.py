from node import Node
from constants import *
import math

class ResourceNode(Node):
    def __init__(self, id, pos, island):
        super().__init__(id, pos)

        self.popped = False
        self.bubble_owner = None

        if island:
            self.bonus = ISLAND_RESOURCE_BONUS
            self.bubble = ISLAND_RESOURCE_BUBBLE
            self.ring_color = PURPLE
        else:
            self.bonus = RESOURCE_BONUS
            self.bubble = RESOURCE_BUBBLE
            self.ring_color = PURPLE

        self.bubble_size = self.bubble

    def capture(self, clicker=None):
        if self.owner:
            self.owner.tick_production -= self.bonus
        super().capture(clicker)
        self.owner.tick_production += self.bonus

    def grow(self):
        pass

    def left_click(self, clicker):
        pass

    def delivery(self, amount, player):
        if not self.popped:
            self.bubble_owner = player
            self.bubble_size -= amount
            if self.bubble_size <= 0:
                self.pop()
        else:
            super().delivery(amount, player)

    def pop(self):
        self.popped = True
        self.capture(self.bubble_owner)
        self.value = self.bubble * 0.44 # 1 - (18 + 5) / (2*18 + 5) = 

    def bubble_controlled(self, owner):
        if self.bubble_owner == None or owner == self.bubble_owner:
            return False
        for edge in self.current_incoming:
            if edge.flowing:
                return True
        return False

    def size_factor(self):
        if not self.popped:
            return max(math.log10(self.bubble/10)/2+self.bubble/1000+0.15,0)/2
        else:
            if self.value<5:
                return 0
            return max(math.log10(self.value/10)/2+self.value/1000+0.15,0)

    @property
    def color(self):
        if not self.popped:
            return GREY
        return super().color

    




