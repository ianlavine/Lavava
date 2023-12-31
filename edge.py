from constants import *

class Edge:

    def __init__(self, to_node, from_node, id):
        self.item_type = EDGE
        self.to_node = to_node
        self.from_node = from_node
        self.id = id
        self.on = False
        self.flowing = False
        self.owned = False
        self.contested = False
        self.popped = False
        self.update_nodes()
        self.state = 'one-way'
        self.type = EDGE

    def __str__(self):
        return str(self.id)

    def update_nodes(self):
        self.to_node.new_edge(self, 'incoming')
        self.from_node.new_edge(self, 'outgoing')

    def click(self, clicker, button):
        if button == 1 and self.owned_by(clicker):
            self.switch()

    def switch(self, specified=None):
        if specified == None:
            self.on = not self.on
        else:
            self.on = specified
        if not self.on:
            self.popped = True

    def update(self):
        if self.from_node.value < MINIMUM_TRANSFER_VALUE or self.flow_check():
            self.flowing = False
        elif self.from_node.value > BEGIN_TRANSFER_VALUE:
            self.flowing = True

        if self.flowing:
            self.flow()
            if not self.popped:
                self.pop()

    def flow_check(self):
        return not self.on or (self.to_node.full and not self.contested)

    def pop(self):
        self.popped = True
        if not self.contested or not AUTO_ATTACK: 
            self.on = False

    def flow(self):
        amount_transferred = TRANSFER_RATE * self.from_node.value
        self.delivery(amount_transferred)
        self.from_node.value -= amount_transferred

    def delivery(self, amount):
        self.to_node.delivery(amount, self.from_node.owner)

    def check_status(self):
        self.owned = False
        self.contested = False
        if self.to_node.owner == None or self.from_node.owner == None:
            return
        elif self.to_node.owner == self.from_node.owner:
            self.owned = True
        else:
            self.contested = True

    def owned_by(self, player):
        return self.from_node.owner == player

    @property
    def color(self):
        if self.on:
            if self.flowing:
                return self.from_node.color
            return self.from_node.color
        return (50, 50, 50)

    def opposite(self, node):
        if node == self.from_node:
            return self.to_node
        return self.from_node
    