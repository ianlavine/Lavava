from edge import Edge
from constants import DYNAMIC_EDGE


class DynamicEdge(Edge):
    def __init__(self, node1, node2, id, initial=False):
        super().__init__(node1, node2, id, initial)
        self.state = "two-way"
        self.item_type = DYNAMIC_EDGE

    def update_nodes(self, initial=False):
        self.to_node.new_edge(self, initial)
        self.from_node.new_edge(self, initial)

    def click_swap(self):
        self.on = True
        self.swap_direction()

    def natural_swap(self):
        self.on = False
        self.swap_direction()

    def swap_direction(self):
        if self.state == "two-way":
            temp = self.to_node
            self.to_node = self.from_node
            self.from_node = temp

    def click(self, clicker, button):
        super().click(clicker, button)
        if button == 3 and self.to_node.owner == clicker:
            # must own the node that will become from_node after swap (to_node becomes from_node)
            # if you don't own both sides, you can only swap when full
            if self.owned:
                self.click_swap()
            elif self.to_node.full():
                self.click_swap()

    def check_status(self):
        if self.from_node.owner is None and self.to_node.owner is not None:
            self.natural_swap()

    def update(self):
        # check to see if edge should swap on its own. This only occurs when its contested.
        # point to the node with a lower status
        # if equal status, only swap if from_node is not full and smaller than to_node*
        # note that if flowing, a slight advantage is given to from_node (momentum)
        super().update()
        if self.contested:
            to_status = self.to_node.swap_status
            from_status = self.from_node.swap_status
            if from_status < to_status:
                self.natural_swap()
            elif to_status == from_status and not self.from_node.full():
                to_value = self.to_node.value
                from_value = self.from_node.value
                if self.flowing:
                    from_value *= 1.05
                if from_value < to_value:
                    self.natural_swap()

    def freeze(self):
        self.state = "one-way"

    def controlled_by(self, player):
        return super().controlled_by(player) or (
            self.to_node.owner == player and self.from_node.owner is None
        )

    def can_be_controlled_by(self, player):
        return self.to_node.owner == player or self.to_node.owner == player
