FLOW = 2

class Edge:

    def __init__(self, to_node, from_node, directed=True):
        self.directed = directed
        self.to_node = to_node
        self.from_node = from_node
        self.opposing_nodes = {to_node.id: from_node, from_node.id: to_node}
        self.flowing = True
        to_node.incoming.append(self)
        from_node.outgoing.append(self)
        if not directed:
            from_node.incoming.append(self)
            to_node.outgoing.append(self)
        self.owned = False

    def lose_ownership(self):
        self.owned = False
        self.flowing = True

    def flow(self):
        if self.directed:
            amount_transferred = self.from_node.value * FLOW
            self.to_node.value += amount_transferred
            self.from_node.value -= amount_transferred

    def change_flow(self):
        self.flowing = not self.flowing
    