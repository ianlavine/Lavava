from abc import ABC, abstractmethod
from constants import *

class Ability(ABC):

    def __init__(self, key, name, cost, color, effect):
        self.key = key
        self.name = name
        self.cost = cost
        self.color = color
        self.effect = effect

    @abstractmethod
    def validate(self, player, node):
        pass

    def input(self, player, data):
        player.money -= self.cost
        return self.effect(data)

    def select(self, player):
        if player.mode == self.key:
            player.mode = 'default'
        elif player.money >= self.cost:
            player.mode = self.key

    def use(self, player, node):
        if data := self.validate(player, node):
            return self.success(player, data)
        return False

    def success(self, player, data):
        player.mode = 'default'
        return (self.key, player.id, data)


class Bridge(Ability):
    def __init__(self, check_new_edge, buy_new_edge):
        super().__init__(BRIDGE_CODE, 'Bridge', BRIDGE_COST, DARK_YELLOW, buy_new_edge)
        self.first_node = None
        self.check_new_edge = check_new_edge

    def validate(self, player, node):
        if self.first_node is not None:
            if new_edge_id := self.check_new_edge(self.first_node, node.id):
                old_node_id = self.first_node
                self.first_node = None
                return (new_edge_id, old_node_id, node.id)
        else:
            if node.owner == player:
                self.first_node = node.id
        return False

    def input(self, data):
        player = self.effect(*data)
        player.money -= self.cost

    def success(self, player, data):
        player.mode = 'default'
        return data


class Nuke(Ability):
    def __init__(self, remove_node):
        super().__init__(NUKE_CODE, 'Nuke', NUKE_COST, BLACK, remove_node)

    def validate(self, player, node):
        if node.owner != player and node.owner is not None:
            return node.id
        return False

        