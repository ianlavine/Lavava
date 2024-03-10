from numpy import sort
from constants import (
    NODE,
    PORT_NODE,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    STATE_NAMES,
    EFFECT_NAMES,
    AUTO_ATTACK,
    AUTO_EXPAND,
    BLACK,
    BROWN,
)
from nodeState import DefaultState, MineState, StartingCapitalState, ZombieState, CapitalState
from nodeEffect import EffectType, Poisoned, NodeEnraged, Burning
import mode
import random
from math import pi, atan2

class Node:
    def __init__(self, id, pos):
        self.value = 0
        self.owner = None
        self.item_type = NODE
        self.edges = set()
        self.id = id
        self.pos = pos
        self.type = NODE
        self.effects = {}
        self.expel_multiplier = 1
        self.intake_multiplier = 1
        self.grow_multiplier = 1
        self.set_default_state()
        self.updated = False

    def __str__(self):
        return str(self.id)

    def new_edge(self, edge, initial):
        self.edges.add(edge)

    def set_state(self, status_name, data=None):
        if status_name in STATE_NAMES:
            self.state = self.new_state(status_name, data)
            self.state_name = status_name
        elif status_name in EFFECT_NAMES:
            self.effects[status_name] = self.new_effect(status_name)
        self.calculate_interactions()

    def new_state(self, state_name, data=None):
        self.updated = True
        if state_name == "default":
            return DefaultState(self.id)
        elif state_name == "mine":
            if data is True and mode.MODE == 3:
                self.port_count = 3
            return MineState(self.id, self.absorbing, data)
        elif state_name == "zombie":
            return ZombieState(self.id)
        elif state_name == "capital":
            if data:
                return StartingCapitalState(self.id)
            return CapitalState(self.id)
        else:
            return DefaultState(self.id)


    def new_effect(self, effect_name):
        if effect_name == 'poison':
            return Poisoned(self.spread_poison)
        elif effect_name == 'rage':
            return NodeEnraged()

    def calculate_interactions(self):
        inter_grow, inter_intake, inter_expel = 1, 1, 1
        for effect in self.effects.values():
            if effect.effect_type == EffectType.GROW:
                inter_grow *= effect.effect(inter_grow)
            elif effect.effect_type == EffectType.INTAKE:
                inter_intake *= effect.effect(inter_intake)
            elif effect.effect_type == EffectType.EXPEL:
                inter_expel *= effect.effect(inter_expel)
        self.grow_multiplier = inter_grow
        self.intake_multiplier = inter_intake
        self.expel_multiplier = inter_expel

    def set_default_state(self):
        self.set_state("default")

    def click(self, clicker, button):
        if button == 1:
            self.left_click(clicker)
        elif button == 3:
            self.right_click()

    def right_click(self):
        pass

    def left_click(self, clicker):
        if self.owner is None:
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
        for edge in self.edges:
            edge.check_status()

    def set_pos_per(self):
        self.pos_x_per = self.pos[0] / SCREEN_WIDTH
        self.pos_y_per = self.pos[1] / SCREEN_HEIGHT

    def relocate(self, width, height):
        self.pos = (self.pos_x_per * width, self.pos_y_per * height)

    def owned_and_alive(self):
        return self.owner is not None and not self.owner.eliminated

    def spread_poison(self):
        for edge in self.outgoing:
            if (
                edge.on
                and not edge.contested
                and edge.to_node.state_name == "default"
            ):
                edge.to_node.set_state("poison")

    def grow(self):
        if self.can_grow():
            self.value += self.state.grow(self.grow_multiplier)
        self.effects_update()

    def can_grow(self):
        ## Gross mention of poison
        ## I could cycle through all effects
        if self.state.can_grow(self.value) or 'poison' in self.effects:
            return True

    def effects_update(self):

        removed_effects = self.effects_tick()

        if removed_effects:
            self.calculate_interactions()

        self.spread_effects()
    
    def effects_tick(self):
        effects_to_remove = [key for key, effect in self.effects.items() if not effect.count()]
        for key in effects_to_remove:
            self.effects[key].complete()
        for key in effects_to_remove:
            del self.effects[key]

        return effects_to_remove

    def spread_effects(self):
        for key, effect in self.effects.items():
            if effect.can_spread_func(effect):
                for edge in self.edges:
                    neighbor = edge.opposite(self)
                    if key not in neighbor.effects and effect.spread_criteria_func(edge, neighbor):
                        neighbor.set_state(key)

    def delivery(self, amount, player):
        self.value += self.state.intake(
            amount, self.intake_multiplier, player != self.owner
        )
        if self.state.flow_ownership:
            self.owner = player
        if self.state.killed(self.value):
            self.capture(player)

    def accept_delivery(self, player):
        return self.state.accept_intake(player != self.owner, self.value)

    def send_amount(self):
        return self.state.expel(self.expel_multiplier, self.value)

    def update_ownerships(self, player=None):
        if self.owner is not None and self.owner != player:
            self.owner.count -= 1
        if player is not None:
            player.count += 1
            player.pass_on_effects(self)
        self.owner = player
        if self.state.update_on_new_owner:
            self.updated = True

    def capture(self, player):
        self.value = self.state.capture_event()(self.value)
        self.update_ownerships(player)
        self.check_edge_stati()
        self.expand()
        if self.state.reset_on_capture:
            self.set_default_state()

    def absorbing(self):
        for edge in self.incoming:
            if edge.flowing:
                return True
        return False

    def acceptBridge(self):
        return self.state.acceptBridge

    @property
    def swap_status(self):
        return self.state.swap_status

    def full(self):
        return self.value >= self.state.full_size

    @property
    def outgoing(self):
        return {edge for edge in self.edges if edge.from_node == self}

    @property
    def incoming(self):
        return {edge for edge in self.edges if edge.to_node == self}

    @property
    def neighbors(self):
        return [edge.opposite(self) for edge in self.edges]

    @property
    def size(self):
        return int(5 + self.state.size_factor(self.value) * 18)

    @property
    def color(self):
        if self.owner:
            return self.owner.color
        return BLACK
    
    # @property
    # def owner_id(self):
    #     return self.owner.id if self.owner else None
    

class PortNode(Node):
    def __init__(self, id, pos, port_count):
        super().__init__(id, pos)
        self.item_type = PORT_NODE
        self.port_count = port_count
        self.ports_angles = []

    @property
    def is_port(self):
        return self.port_count != 0

    def new_effect(self, effect_name):
        if effect_name == 'burn':
            return Burning(self.lose_ports)
        else:
            return super().new_effect(effect_name)

    def acceptBridge(self):
        return self.port_count > 0 and 'burn' not in self.effects and self.state.acceptBridge

    def new_edge(self, edge, initial):
        if not initial and edge not in self.edges:
            self.port_count -= 1
        super().new_edge(edge, initial)

    def lose_ports(self):
        self.port_count = 0

    @property
    def color(self):
        if self.owner:
            return self.owner.color
        elif self.is_port:
            return BROWN
        return BLACK
    
    def set_port_angles(self, min_angular_distance=0.4):
        """
        Determines and sets the angles for the ports, ensuring they do not overlap with each other or the edges extending from the node.
        `min_angular_distance` is the minimum angular distance between ports and between ports and edges.
        Returns a list of two angles for the ports.
        """

        # choose two randomly spaced out angles
        first = random.uniform(0, pi)
        second = first + pi
        self.ports_angles = [first, second]

        # edge_angles = self.calculate_edge_angles()
        # valid_angles = self.find_valid_angles(edge_angles, min_angular_distance)

        # opts = []
        # if len(valid_angles) == 1:
        #     opts = valid_angles[0]
        # elif len(valid_angles) > 1:
        #     opts = sorted(valid_angles, key=len, reverse=True)[:2]
        #     if len(opts[0]) > len(opts[1]) * 2:
        #         opts = [opts[0]]

        #     rf = len(opts) // 3
        #     rs = (len(opts) // 3) * 2
        #     self.ports_angles = [opts[rf], opts[rs]]
        # elif len(valid_angles) > 1:

            
        #     self.ports_angles = [opts[0][len(opts[0]) // 2], opts[1][len(opts[1]) // 2]]
            
        # else:
        #     # Fallback if no valid angles found - consider a more sophisticated approach
        #     self.ports_angles = [random.uniform(0, 2 * pi), random.uniform(0, 2 * pi)]

    def calculate_edge_angles(self):
        """
        Calculates and returns a list of angles for all edges connected to this node.
        """
        angles = []
        for edge in self.edges:
            other_node = edge.opposite(self)
            dx = other_node.pos[0] - self.pos[0]
            dy = other_node.pos[1] - self.pos[1]
            angle = atan2(dy, dx)
            angles.append(angle)
        
        return angles

    def find_valid_angles(self, edge_angles, min_angular_distance):
        """
        Finds valid angles for ports that do not overlap with existing edge angles.
        """
        valid_angles = []
        sub_edges = []
        for angle in [i * min_angular_distance for i in range(int(2 * pi / (min_angular_distance / 4)))]:
            if all(abs(angle - edge_angle) >= min_angular_distance for edge_angle in edge_angles):
                sub_edges.append(angle)
            elif len(sub_edges) >= 1:
                valid_angles.append(sub_edges.copy())
                sub_edges.clear()
        if len(sub_edges) >= 1:
            if len(valid_angles) == 0:
                valid_angles.append(sub_edges.copy())
            else:
                valid_angles[0] = sort(valid_angles[0] + sub_edges.copy())
        return valid_angles

    def find_next_valid_angle(self, base_angle, valid_angles, min_angular_distance):
        """
        Finds the next valid angle for the second port, ensuring minimum angular distance from the first port's angle.
        """
        for angle in valid_angles:
            if abs(angle - base_angle) >= min_angular_distance:
                return angle
        # Fallback, might need a better solution if this scenario is likely
        return base_angle + min_angular_distance
