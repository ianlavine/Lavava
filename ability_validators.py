from constants import CONTEXT


def no_click(data):
    return False

def standard_node_attack(data):
    node = data[0]
    return node.owner != CONTEXT['main_player'] and node.owner is not None \
        and node.state_name not in ['capital', 'mine']

def dynamic_edge_own_either(data):
    edge = data[0]
    return edge.state == 'two-way' and \
        (edge.from_node.owner == CONTEXT['main_player'])

def capital_logic(data):
    node = data[0]
    if node.owner == CONTEXT['main_player'] and node.state_name != 'capital' and node.full:
        neighbor_capital = False
        for neighbor in node.neighbors:
            if neighbor.state_name == 'capital':
                neighbor_capital = True
                break
        if not neighbor_capital:
            return True
    return False

def standard_port_node(data):
    node = data[0]
    return node.owner is not None and node.is_port and node.state_name not in ['mine']

def unowned_node(data):
    node = data[0]
    return node.owner is None and node.state_name not in ['mine']

def new_edge_validator(check_new_edge):

    def new_edge_standard(data):
        if len(data) == 1:
            first_node = data[0]
            return first_node.owner == CONTEXT['main_player']
        else:
            first_node, second_node = data[0], data[1]
            return first_node.id != second_node.id and check_new_edge(first_node.id, second_node.id)

    def new_edge_ports(data):
        return data[0].port_count > 0 and new_edge_standard(data)

    if CONTEXT['mode'] == 3:
        return new_edge_ports
    return new_edge_standard