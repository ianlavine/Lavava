from collections import defaultdict
from constants import *
from helpers import *
from edge import Edge
from dynamicEdge import DynamicEdge

class Board:

    def __init__(self):
        self.nodes = []
        self.edges = []
        self.edge_dict = defaultdict(set)
        self.id_dict = {}
        self.extra_edges = 2
        self.highlighted = None
        self.highlighted_color = None

    def rage(self, player):
        for edge in self.edges:
            if edge.can_be_owned_by(player):
                edge.enrage()

    def reset(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges
        self.edge_dict = defaultdict(set)
        self.expand_nodes()
        self.id_dict = {node.id: node for node in self.nodes} | {edge.id: edge for edge in self.edges}
        self.extra_edges = 2

    def check_highlight(self, position, ability_manager):
        self.highlighted_color = ability_manager.box.color
        self.highlighted = self.hover(position, ability_manager)

    def validate(self, ability_manager, id):
        if ability_manager.mode == DEFAULT_ABILITY_CODE:
            if not ability_manager.default_validate():
                return False
        return ability_manager.ability.validate(self.id_dict[id])

    def hover(self, position, ability_manager):
        ability = ability_manager.ability
        if id := self.find_node(position):
            if ability.click_type == NODE and self.validate(ability_manager, id): 
                return self.id_dict[id]
        elif id := self.find_edge(position):
            if ability.click_type == EDGE and self.validate(ability_manager, id):
                return self.id_dict[id]
            elif self.id_dict[id].owned_by(CONTEXT['main_player']):
                self.highlighted_color = GREY
                return self.id_dict[id]
        return None

    def click_edge(self):
        if self.highlighted.type == EDGE:
            return self.highlighted.id
        return False

    def eliminate(self, player):
        for edge in self.edges:
            if edge.owned_by(player):
                edge.switch(False)

    def expand_nodes(self):

        far_left_node = min(self.nodes, key=lambda node: node.pos[0])
        far_right_node = max(self.nodes, key=lambda node: node.pos[0])

        far_left_x = far_left_node.pos[0]
        far_right_x = far_right_node.pos[0]

        original_width = far_right_x - far_left_x
        new_width = SCREEN_WIDTH *  (1 - ABILITY_GAP)
        scaling_factor = new_width / original_width if original_width != 0 else 1

        for node in self.nodes:
            x, y = node.pos
            new_x = 25 + (x - far_left_x) * scaling_factor
            node.pos = (new_x, y)
            node.set_pos_per()

    def update(self):
        for spot in self.nodes:
            if spot.owned_and_alive():  # keep 
                spot.grow()

        for edge in self.edges:
            edge.update()

    def find_node(self, position):
        for node in self.nodes:
            if ((position[0] - node.pos[0])**2 + (position[1] - node.pos[1])**2) <= (node.size) ** 2+3:
                return node.id
        return None

    def find_edge(self, position):
        for edge in self.edges:
            if distance_point_to_segment(position[0],position[1],edge.from_node.pos[0],edge.from_node.pos[1],edge.to_node.pos[0],edge.to_node.pos[1]) < 5:
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
        return NODE_COUNT + EDGE_COUNT + self.extra_edges + self.id_dict[node_from].owner.id

    def check_all_overlaps(self, edge):

        edgeDict = defaultdict(set)
        self.nodeDict = {node.id: (node.pos) for node in self.nodes}
        for e in self.edges:
            edgeDict[e.to_node.id].add(e.from_node.id)
            edgeDict[e.from_node.id].add(e.to_node.id)

        for key in edgeDict:
            for val in edgeDict[key]:
                if edge[0]!=val and edge[0]!=key and edge[1]!=val and edge[1]!=key:
                    if self.overlap(edge, (key, val)):
                        return False
        return True

    def overlap(self, edge1, edge2):
        
        return do_intersect(self.nodeDict[edge1[0]],self.nodeDict[edge1[1]],self.nodeDict[edge2[0]],self.nodeDict[edge2[1]])
        
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

    def safe_remove(self, lst, value):
        try:
            lst.remove(value)
        except ValueError:
            pass

    def remove_node(self, node_id):
        node = self.id_dict[node_id]
        node.owner.count -= 1
        for edge in node.outgoing + node.incoming:
            opp = edge.opposite(node)
            self.safe_remove(opp.incoming, edge)
            self.safe_remove(opp.incoming, edge)
            if edge.id in self.id_dict:
                self.id_dict.pop(edge.id)
                self.edges.remove(edge)
        self.id_dict.pop(node_id)
        self.nodes.remove(node)