from edge import Edge
from constants import DYNAMIC_EDGE

class DynamicEdge(Edge):
    def __init__(self, node1, node2, id):
        super().__init__(node1, node2, id)
        self.state = 'two-way'
        self.item_type = DYNAMIC_EDGE

    def update_nodes(self):
        self.to_node.new_edge(self, 'incoming')
        self.from_node.new_edge(self, 'outgoing')
        self.to_node.new_edge(self, 'outgoing')
        self.from_node.new_edge(self, 'incoming')

    def click_swap(self):
        self.on = True
        self.swap_direction

    def natural_swap(self):
        self.on = False
        self.swap_direction()

    def swap_direction(self):
        if self.state == 'two-way':
            temp = self.to_node
            self.to_node = self.from_node
            self.from_node = temp

    def click(self, clicker, button):
        super().click(clicker, button)
        if button == 3:
            if not self.contested and self.to_node.owner == clicker or self.from_node.owner == clicker:
                self.click_swap()

    def check_status(self):
        self.owned = False
        self.contested = False
        if self.to_node.owner == None or self.from_node.owner == None:
            if self.from_node.owner is None:
                self.natural_swap()
            return
        elif self.to_node.owner == self.from_node.owner:
            self.owned = True
        else:
            self.contested = True

    def update(self):
        super().update()
        if self.contested:
            if self.to_node.value > self.from_node.value:
                self.natural_swap()

    def freeze(self):
        self.state = 'one-way'

    def owned_by(self, player):
        return super().owned_by(player) or (self.to_node.owner == player and self.from_node.owner is None)

    def can_be_owned_by(self, player):
        return self.to_node.owner == player or self.to_node.owner == player
    


    