from constants import CANNON_SHOT_CODE, MINIMUM_TRANSFER_VALUE, SPAWN_CODE, BRIDGE_CODE, D_BRIDGE_CODE, POISON_CODE, NUKE_CODE, CAPITAL_CODE, BURN_CODE, FREEZE_CODE, RAGE_CODE, STANDARD_LEFT_CLICK, STANDARD_RIGHT_CLICK, ZOMBIE_CODE, CANNON_CODE, NUKE_RANGE


def no_click(data):
    return True

def standard_port_node(data):
    node = data[0]
    return node.owner is not None and node.is_port and node.state_name not in ["mine"]

def unowned_node(data):
    node = data[0]
    return node.owner is None and node.state_name == "default"

def standard_node_attack(data, player):
    node = data[0]
    return (
        node.owner != player
        and node.owner is not None
        and node.state_name not in ["capital", "mine"]
    )


def attack_validators(capital_func, player):

    def capital_ranged_node_attack(data):
        node = data[0]
        capitals = capital_func[player]

        def in_capital_range(capital):
            x1, y1 = node.pos
            x2, y2 = capital.pos
            distance = (x1 - x2) ** 2 + (y1 - y2) ** 2
            capital_nuke_range = (NUKE_RANGE * capital.value) ** 2
            return distance <= capital_nuke_range

        return standard_node_attack(node, player) and any(in_capital_range(capital) for capital in capitals)

    return capital_ranged_node_attack


def validators_needing_player(player):

    def capital_logic(data):
        node = data[0]
        if (
            node.owner == player
            and node.state_name != "capital"
            and node.full()
        ):
            neighbor_capital = False
            for neighbor in node.neighbors:
                if neighbor.state_name == "capital":
                    neighbor_capital = True
                    break
            if not neighbor_capital:
                return True
        return False
    
    def my_node(data):
        node = data[0]
        return node.owner == player
    
    def attacking_edge(data):
        edge = data[0]
        return edge.from_node.owner == player and standard_node_attack(edge.to_node, player)

    def dynamic_edge_own_either(data):
        edge = data[0]
        return edge.dynamic and (edge.from_node.owner == player)
    
    return {
        CAPITAL_CODE: capital_logic,
        POISON_CODE: attacking_edge,
        FREEZE_CODE: dynamic_edge_own_either,
        ZOMBIE_CODE: my_node,
        CANNON_CODE: my_node,
    }


def crossover_validators(check_new_edge, player=None):
    def no_crossovers(data, override_player=player):
        first_node, second_node = data[0], data[1]
        return first_node.owner == override_player and first_node.id != second_node.id and check_new_edge(
            first_node.id, second_node.id
        )

    def new_edge_ports(data):
        if all([node.is_port for node in data]):
            return no_crossovers(data)
        return False
    
    def cannon_shot_check(self, override_player, data):
        cannon, target = self.id_dict[data[0]], self.id_dict[data[1]]
        can_shoot = cannon.state_name == "cannon" and cannon.owner == override_player
        can_accept = cannon.value > MINIMUM_TRANSFER_VALUE and (target.owner != override_player or not target.full())
        return can_shoot and can_accept and no_crossovers(data, override_player)

    return (new_edge_ports, cannon_shot_check)





def make_ability_validators(board, player):
    return {
        SPAWN_CODE: unowned_node,
        BRIDGE_CODE: crossover_validators(board.check_new_edge, player)[0],
        D_BRIDGE_CODE: crossover_validators(board.check_new_edge, player)[0],
        BURN_CODE: standard_port_node,
        RAGE_CODE: no_click,
        NUKE_CODE: attack_validators(board.player_capitals, player),
    } | validators_needing_player(player)


def make_effect_validators(board):
    return {
        CANNON_SHOT_CODE: crossover_validators(board.check_new_edge)[1],
        STANDARD_LEFT_CLICK: lambda player, data: board.id_dict[data[0]].valid_left_click(player),
        STANDARD_RIGHT_CLICK: lambda player, data: board.id_dict[data[0]].valid_right_click(player),
    }
