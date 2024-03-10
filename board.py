from collections import defaultdict
from constants import (
    DEFAULT_ABILITY_CODE,
    EDGE,
    DYNAMIC_EDGE,
    GREY,
    SCREEN_WIDTH,
    HORIZONTAL_ABILITY_GAP,
    NODE_COUNT,
    EDGE_COUNT,
    CONTEXT,
    NODE,
    PORT_NODE,
)
from helpers import distance_point_to_segment, do_intersect
from edge import Edge
from dynamicEdge import DynamicEdge
from gameStateEnums import GameStateEnum as GSE
from tracker import Tracker


class Board:
    def __init__(self, gs):
        self.gs = gs
        self.nodes = []
        self.edges = []
        self.edge_dict = defaultdict(set)
        self.id_dict = {}
        self.extra_edges = 2
        self.highlighted = None
        self.highlighted_color = None
        self.tracker = Tracker()
        self.player_capitals = defaultdict(set)

    def board_wide_effect(self, player, effect):
        for node in self.nodes:
            if node.owner == player:
                node.set_state(effect)

    def track_starting_states(self):
        for node in self.nodes:
            if node.state_name != "default":
                self.tracker.node(node)

    def track_state_changes(self, nodes):

        self.player_capitals.clear()

        for node in nodes:
            self.tracker.node(node)
            node.updated = False

        for id in self.tracker.tracked_id_states:
            node = self.id_dict[id]
            if node.state_name == "capital" and node.owner:
                self.player_capitals[node.owner].add(node)

    def reset(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges
        self.edge_dict = defaultdict(set)
        self.expand_nodes()
        # Gross. Mode Ports as a boolean could be used in multiple places
        self.set_all_ports()
        if self.nodes[0].item_type == PORT_NODE:
            for node in self.nodes:
                node.set_port_angles()
        self.id_dict = {node.id: node for node in self.nodes} | {
            edge.id: edge for edge in self.edges
        }
        self.extra_edges = 2
        self.tracker.reset()
        self.player_capitals.clear()
        self.track_starting_states()

    def set_all_ports(self):
        if self.nodes[0].item_type == PORT_NODE:
            for node in self.nodes:
                node.set_port_angles()

    ## Gross code. Needs to be refactored
    def check_highlight(self, position, ability_manager):
        self.highlighted_color = None
        self.highlighted = self.hover(position, ability_manager)
        if self.highlighted and not self.highlighted_color:
            if self.default_highlight_color(ability_manager):
                self.highlighted_color = CONTEXT["main_player"].default_color
            else:
                self.highlighted_color = ability_manager.box_col

    # Still gross
    def default_highlight_color(self, ability_manager):
        return (
            (self.gs.state.value < GSE.PLAY.value)
            or (not ability_manager.ability)
            or (ability_manager.ability.click_type != self.highlighted.type)
        )

    # Still gross
    def hover(self, position, ability_manager):
        ability = ability_manager.ability
        if id := self.find_node(position):
            if (not ability) or ability.click_type == NODE:
                if (
                    self.gs.state.value < GSE.PLAY.value
                    and self.id_dict[id].owner is None
                    and self.id_dict[id].state_name == "default"
                ):
                    return self.id_dict[id]
                elif ability and ability.validate(self.id_dict[id]):
                    return self.id_dict[id]
        elif id := self.find_edge(position):
            if (
                ability
                and ability.click_type == EDGE
                and ability.validate(self.id_dict[id])
            ):
                return self.id_dict[id]
            elif self.id_dict[id].controlled_by(CONTEXT["main_player"]) or (
                self.id_dict[id].to_node.owner == CONTEXT["main_player"]
                and self.id_dict[id].to_node.full()
            ):
                self.highlighted_color = GREY
                return self.id_dict[id]
        return None

    ## Gross code ends here (I hope)

    def click_edge(self):
        if self.highlighted and self.highlighted.type == EDGE:
            return self.highlighted.id
        return False

    def eliminate(self, player):
        for edge in self.edges:
            if edge.controlled_by(player):
                edge.switch(False)

    def expand_nodes(self):
        far_left_node = min(self.nodes, key=lambda node: node.pos[0])
        far_right_node = max(self.nodes, key=lambda node: node.pos[0])

        far_left_x = far_left_node.pos[0]
        far_right_x = far_right_node.pos[0]

        original_width = far_right_x - far_left_x
        new_width = SCREEN_WIDTH * (1 - HORIZONTAL_ABILITY_GAP)
        scaling_factor = new_width / original_width if original_width != 0 else 1

        for node in self.nodes:
            x, y = node.pos
            new_x = 25 + (x - far_left_x) * scaling_factor
            node.pos = (new_x, y)
            node.set_pos_per()

    def update(self):
        updated_nodes = []

        for spot in self.nodes:
            if spot.owned_and_alive():  # keep
                spot.grow()
            if spot.updated:
                updated_nodes.append(spot)

        for edge in self.edges:
            edge.update()

        if updated_nodes:
            self.track_state_changes(updated_nodes)

        for player in self.player_capitals:
            player.full_capital_count = len([n for n in self.player_capitals[player] if n.full()])

    def find_node(self, position):
        for node in self.nodes:
            if (
                (position[0] - node.pos[0]) ** 2 + (position[1] - node.pos[1]) ** 2
            ) <= (node.size) ** 2 + 3:
                return node.id
        return None

    def find_edge(self, position):
        for edge in self.edges:
            if (
                distance_point_to_segment(
                    position[0],
                    position[1],
                    edge.from_node.pos[0],
                    edge.from_node.pos[1],
                    edge.to_node.pos[0],
                    edge.to_node.pos[1],
                )
                < 5
            ):
                return edge.id
        return None

    def check_new_edge(self, node_from, node_to):
        if node_to == node_from:
            return False
        edge_set = {(edge.from_node.id, edge.to_node.id) for edge in self.edges}
        if (node_to, node_from) in edge_set or (node_from, node_to) in edge_set:
            return False
        if not self.check_all_overlaps((node_to, node_from)):
            return False
        return True

    def new_edge_id(self, node_from):
        return (
            NODE_COUNT
            + EDGE_COUNT
            + self.extra_edges
            + self.id_dict[node_from].owner.id
        )

    def check_all_overlaps(self, edge):
        edgeDict = defaultdict(set)
        self.nodeDict = {node.id: (node.pos) for node in self.nodes}
        for e in self.edges:
            edgeDict[e.to_node.id].add(e.from_node.id)
            edgeDict[e.from_node.id].add(e.to_node.id)

        for key in edgeDict:
            for val in edgeDict[key]:
                if (
                    edge[0] != val
                    and edge[0] != key
                    and edge[1] != val
                    and edge[1] != key
                ):
                    if self.overlap(edge, (key, val)):
                        return False
        return True

    def overlap(self, edge1, edge2):
        return do_intersect(
            self.nodeDict[edge1[0]],
            self.nodeDict[edge1[1]],
            self.nodeDict[edge2[0]],
            self.nodeDict[edge2[1]],
        )

    def buy_new_edge(self, id, node_from, node_to, edge_type):
        if edge_type == DYNAMIC_EDGE:
            newEdge = DynamicEdge(self.id_dict[node_to], self.id_dict[node_from], id)
        else:
            newEdge = Edge(self.id_dict[node_to], self.id_dict[node_from], id)

        newEdge.check_status()
        newEdge.popped = True
        newEdge.switch(True)
        self.edges.append(newEdge)
        self.id_dict[newEdge.id] = newEdge
        self.extra_edges += 5

    def remove_node(self, node):
        node.owner.count -= 1
        for edge in node.edges:
            opp = edge.opposite(node)
            opp.incoming.discard(edge)
            opp.outgoing.discard(edge)
            if edge.id in self.id_dict:
                self.id_dict.pop(edge.id)
                self.edges.remove(edge)
        self.id_dict.pop(node.id)
        self.nodes.remove(node)

    @property
    def percent_energy(self):
        self_energy = 0
        energy = 0.01
        for node in self.nodes:
            if node.owner == CONTEXT["main_player"]:
                self_energy += node.value
            if node.owned_and_alive():
                energy += node.value
        return int(self_energy * 100 / energy)
