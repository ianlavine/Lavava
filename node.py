from constants import *
from state_builder import set_node_state
from nodeState import *
from nodeEffect import *

class Node:

    def __init__(self, id, pos):
        self.value = 0
        self.owner = None
        self.item_type = NODE
        self.incoming = []
        self.outgoing = []
        self.id = id
        self.pos = pos
        self.type = NODE
        self.effects = {}
        self.expel_multiplier = 1
        self.intake_multiplier = 1
        self.grow_multiplier = 1
        self.set_default_state()

    def __str__(self):
        return str(self.id)

    def new_edge(self, edge, dir):
        if dir == 'incoming':
            self.incoming.append(edge)
        else:
            self.outgoing.append(edge)

    def set_state(self, status_name, data=None):
        if status_name in STATE_NAMES:
            self.state = self.new_state(status_name, data)
            self.state_name = status_name
        elif status_name in EFFECT_NAMES:
            self.effects[status_name] = self.new_effect(status_name)
        self.calculate_interactions()

    def new_state(self, state_name, data=None):
        if state_name == 'default':
            return DefaultState(self.id)
        elif state_name == "mine":
            if data == True and CONTEXT['mode'] == 3:
                self.port_count = 3
            return MineState(self.id, self.absorbing, data)
        elif state_name == "capital":
            CapitalStateType = MODE['capital']
            return CapitalStateType(self.id)

    def new_effect(self, effect_name):
        if effect_name == 'poison':
            return Poisoned(self, self.spread_poison)
        elif effect_name == 'rage':
            return Enraged(self)

    def calculate_interactions(self):
        inter_grow, inter_intake, inter_expel = 1, 1, 1
        for effect in self.effects.values():
            if effect.effect_type == EffectType.GROW: 
                inter_grow *= effect.effect()
            elif effect.effect_type == EffectType.INTAKE:
                inter_intake *= effect.effect()
            elif effect.effect_type == EffectType.EXPEL:
                inter_expel *= effect.effect()
        self.grow_multiplier = inter_grow
        self.intake_multiplier = inter_intake
        self.expel_multiplier = inter_expel

    def set_default_state(self):
        self.set_state('default')

    def click(self, clicker, button):
        if button == 1:
            self.left_click(clicker)
        elif button == 3:
            self.right_click()

    def right_click(self):
        pass

    def left_click(self, clicker):
        if self.owner == None:
            if clicker.buy_node():
                self.capture(clicker)

    def expand(self):
        for edge in self.outgoing:
            if edge.contested:
                if AUTO_ATTACK:
                    edge.switch(True)
                    edge.popped = True
            elif not edge.owned and AUTO_EXPAND:
                edge.switch(True)
                edge.popped = False

    def check_edge_stati(self):
        for edge in self.incoming:
            edge.check_status()
        for edge in self.outgoing:
            edge.check_status()

    def set_pos_per(self):
        self.pos_x_per = self.pos[0] / SCREEN_WIDTH
        self.pos_y_per = self.pos[1] / SCREEN_HEIGHT

    def relocate(self, width, height):
        self.pos = (self.pos_x_per * width, self.pos_y_per * height)

    def owned_and_alive(self):
        return self.owner != None and not self.owner.eliminated

    def spread_poison(self):
        for edge in self.outgoing:
            if edge.to_node != self and edge.on and not edge.contested and edge.to_node.state_name == 'default':
                edge.to_node.set_state('poisoned')

    def spread_rage(self):
        for edge in self.outgoing:
            if not edge.raged:
                edge.enrage()

    def grow(self):
        if self.value < self.state.full_size:
            self.value += self.state.grow(self.grow_multiplier)
        self.effects_tick()

    def effects_tick(self):
        expired_effects = {}
        for key, effect in self.effects.items():
            effect.count()
            if effect.expired:
                expired_effects.add(key)

        if expired_effects:
            for key in expired_effects:
                self.effects.pop(key)
            self.calculate_interactions()

    def delivery(self, amount, player):
        self.value += self.state.intake(amount, self.intake_multiplier, player == self.owner)
        if self.state.killed(self.value):
            self.capture(player)
        if player.raged:
            self.spread_rage()

    def accept_delivery(self, player):
        return self.state.accept_intake(player == self.owner, self.value)

    def send_amount(self):
        return self.state.expel(self.expel_multiplier)

    def update_ownerships(self, player):
        if self.owner != None:
            self.owner.count -= 1
        player.count += 1
        self.owner = player

    def capture(self, player):
        self.value *= self.state.capture_event()
        self.update_ownerships(player)
        self.check_edge_stati()
        self.expand()
        if self.state.reset_on_capture:
            self.set_default_state()

    def absorbing(self):
        for edge in self.current_incoming:
            if edge.flowing:
                return True
        return False

    def acceptBridge(self):
        return self.state.acceptBridge

    @property
    def full(self):
        return self.value >= GROWTH_STOP

    @property
    def edges(self):
        return self.incoming + self.outgoing

    @property
    def current_incoming(self):
        return [edge for edge in self.incoming if edge.to_node == self]

    @property
    def neighbors(self):
        return [edge.opposite(self) for edge in self.edges]

    @property
    def size(self):
        return int(5+self.state.size_factor(self.value)*18)

    @property
    def color(self):
        if self.owner:
            return self.owner.color
        return BLACK


class PortNode(Node):

    def __init__(self, id, pos, port_count):
        super().__init__(id, pos)
        self.item_type = PORT_NODE
        self.port_count = port_count

    @property
    def is_port(self):
        return self.port_count != 0

    def new_effect(self, effect_name):
        if effect_name == 'burn':
            return Burning(self, self.lose_ports)
        else:
            return super().new_effect(effect_name)

    def acceptBridge(self):
        return self.port_count > 0 and not self.on_fire and self.state.acceptBridge

    def new_edge(self, edge, dir):
        if CONTEXT['started'] and edge not in self.edges and dir == 'outgoing':
            self.port_count -= 1
        super().new_edge(edge, dir)

    @property
    def on_fire(self):
        return 'burn' in self.effects

    def grow(self):
        if self.on_fire:
            self.burning -= 1
            if not self.on_fire:
                self.lose_ports()
        super().grow()

    def lose_ports(self):
        self.port_count = 0

    @property
    def color(self):
        if self.owner:
            return self.owner.color
        elif self.is_port:
            return BROWN
        return BLACK

    