GROWTH_RATE = 0.0001
TRANSFER_RATE = 0.01
ATTACK_PERCENTAGE = 0.5
BLACK = (0, 0, 0)

class Node:

    def __init__(self, id, pos):
        self.value = 0
        self.owner = None
        self.clicker = None
        self.edges = []
        self.id = id
        self.pos = pos

    def __str__(self):
        return str(self.id)

    def grow(self):
        self.value += GROWTH_RATE
        self.owner.score += GROWTH_RATE

    def click(self, clicker):
        self.clicker = clicker
        if self.owner == None:
            if not clicker.begun:
                self.owner = clicker
                clicker.begun = True
                print("First node owned: " + str(self))
                return True
            else:
                return self.expand()
        elif self.owner == clicker:
            self.absorb()
        else:
            self.capture()
        return False

    def absorb(self):
        for edge in self.edges:
            if edge.owned:
                self.share(edge)

    def neighbor(self, edge):
        return edge.opposing_nodes[self.id]

    def expand(self):
        success = False
        print("ATTEMPT: " + str(self) + "------------------")
        for edge in self.edges:
            if self.neighbor(edge).owner == self.clicker:
                print("EXPANDED from: " + str(self.neighbor(edge)))
                edge.owned = True
                success = True
                self.share(edge)
        
        if success:
            self.owner = self.clicker

        return success

    def capture(self):
        attack_edges = []
        broken_edges = []
        attack_strength = 0

        for edge in self.edges:
            neighbor = self.neighbor(edge)
            if neighbor.owner == self.clicker:
                attack_add_on = ATTACK_PERCENTAGE * self.value
                attack_edges.append((edge, attack_add_on))
                attack_strength += attack_add_on
            elif edge.owned:
                broken_edges.append(edge)

        if attack_strength > self.value:
            self.handover(attack_edges, broken_edges)


    def handover(self, attack_edges, broken_edges):
        self.owner = self.clicker
        self.value = 0

        for attack in attack_edges:
            attack[0].owned = True
            self.transfer(self.neighbor(attack[0]), attack[1])

        for edge in broken_edges:
            edge.lose_ownership()

    def share(self, edge):
        neighbor = self.neighbor(edge)
        transfer_amount = neighbor.value * TRANSFER_RATE * edge.flow 
        self.transfer(neighbor, transfer_amount)

    def transfer(self, neighbor, amount):
        self.value += amount
        neighbor.value -= amount

    @property
    def color(self):
        if self.owner:
            return self.owner.color
        return BLACK

        
        
