from collections import defaultdict
from player import Player
from constants import *
from helpers import *
from edge import Edge

class Board:

    def __init__(self, player_count, nodes, edges):

        self.nodes = nodes
        self.edges = edges
        self.player_count = player_count

        self.expand_nodes()

        self.id_dict = {node.id: node for node in self.nodes} | {edge.id: edge for edge in self.edges}
        self.player_dict = {i: Player(COLOR_DICT[i], i) for i in range(player_count)}

        self.remaining = {i for i in range(player_count)}
        self.victor = None

        self.timer = 60

    def eliminate(self, player):
        self.remaining.remove(player)
        for edge in self.edges:
            if edge.owned_by(self.player_dict[player]):
                edge.switch(False)
        self.player_dict[player].eliminate()

    def check_over(self):
        if len(self.remaining) == 1:
            self.victor = self.player_dict[list(self.remaining)[0]]
            self.victor.win()

    def expand_nodes(self):

        far_left_node = min(self.nodes, key=lambda node: node.pos[0])
        far_right_node = max(self.nodes, key=lambda node: node.pos[0])

        far_left_x = far_left_node.pos[0]
        far_right_x = far_right_node.pos[0]

        original_width = far_right_x - far_left_x
        new_width = SCREEN_WIDTH - 50
        scaling_factor = new_width / original_width if original_width != 0 else 1

        for node in self.nodes:
            x, y = node.pos
            new_x = 25 + (x - far_left_x) * scaling_factor
            node.pos = (new_x, y)

    def update(self):

        if self.timer > 0:
            self.timer -= 0.1

            if self.timer > 3 and self.opening_moves == len(self.remaining) * 2:
                self.timer = 3

        else:
            for spot in self.nodes:
                if spot.owned_and_alive():
                    spot.grow()

            for edge in self.edges:
                edge.update()
            
            for player in self.player_dict.values():
                out = player.update()
                if out:
                    self.eliminate(player.id)

            self.check_over()

    def find_node(self, position):
        for node in self.nodes:
            if ((position[0] - node.pos[0])**2 + (position[1] - node.pos[1])**2) < (node.size) ** 2:
                return node.id
        return None

    def find_edge(self, position):
        for edge in self.edges:
            if distance_point_to_segment(position[0],position[1],edge.from_node.pos[0],edge.from_node.pos[1],edge.to_node.pos[0],edge.to_node.pos[1]) < 5:
                return edge.id
        return None

    @property
    def opening_moves(self):
        return sum([player.count for player in self.player_dict.values()])