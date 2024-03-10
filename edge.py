from constants import (
    EDGE,
    MINIMUM_TRANSFER_VALUE,
    BEGIN_TRANSFER_VALUE,
    AUTO_ATTACK,
)


class Edge:
    def __init__(self, to_node, from_node, id, initial=False):
        self.item_type = EDGE
        self.to_node = to_node
        self.from_node = from_node
        self.id = id
        self.on = False
        self.flowing = False
        self.popped = False
        self.update_nodes(initial)
        self.state = "one-way"
        self.type = EDGE

    def __str__(self):
        return str(self.id)

    def update_nodes(self, initial):
        self.to_node.new_edge(self, initial)
        self.from_node.new_edge(self, initial)

    def click(self, clicker, button):
        if button == 1 and self.controlled_by(clicker):
            self.switch()

    def switch(self, specified=None):
        if specified is None:
            self.on = not self.on
        else:
            self.on = specified
        if not self.on:
            self.popped = True

    def update(self):
        if (
            not self.on
            or self.from_node.value < MINIMUM_TRANSFER_VALUE
            or not self.flow_allowed()
        ):
            self.flowing = False
        elif self.from_node.value > BEGIN_TRANSFER_VALUE:
            self.flowing = True

        if self.flowing:
            self.flow()
            if not self.popped:
                self.pop()

    def flow_allowed(self):
        return self.to_node.accept_delivery(self.owner)

    def pop(self):
        self.popped = True
        if not self.contested or not AUTO_ATTACK:
            self.on = False

    def flow(self):
        amount_transferred = self.from_node.send_amount()
        self.delivery(amount_transferred)
        self.from_node.value -= amount_transferred

    def delivery(self, amount):
        self.to_node.delivery(amount, self.from_node.owner)

    def check_status(self):
        pass

    def controlled_by(self, player):
        return self.from_node.owner == player

    def can_be_controlled_by(self, player):
        return self.controlled_by(player)

    @property
    def owned(self):
        return self.duo_ownership and self.to_node.owner == self.from_node.owner

    @property
    def duo_ownership(self):
        return self.to_node.owner is not None and self.from_node.owner is not None

    @property
    def contested(self):
        return self.duo_ownership and self.to_node.owner != self.from_node.owner

    @property
    def owner(self):
        return self.from_node.owner

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
