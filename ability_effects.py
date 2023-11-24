from constants import *

def make_bridge(buy_new_edge, bridge_type):
    def bridge_effect(data, player):
        id1, id2, id3 = data
        buy_new_edge(id1, id2.id, id3.id, bridge_type)
    return bridge_effect

def make_nuke(remove_node):
    def nuke_effect(data, player):
        node = data[0]
        remove_node(node.id)
    return nuke_effect

def make_rage(rage):
    def rage_effect(data, player):
        rage(player)
        player.enrage()
    return rage_effect

def freeze_effect(data, player):
    edge = data[0]
    # if player != edge.from_node.owner:
    #     edge.swap_direction()
    edge.freeze()

def spawn_effect(data, player):
    node = data[0]
    node.capture(player)

def poison_effect(data, player):
    node = data[0]
    node.set_state('poisoned')

def burn_effect(data, player):
    node = data[0]
    node.burn()

def capital_effect(data, player):
    node = data[0]
    node.set_state('capital')

def make_ability_effects(board):
    return {BRIDGE_CODE: make_bridge(board.buy_new_edge, EDGE),
         D_BRIDGE_CODE: make_bridge(board.buy_new_edge, DYNAMIC_EDGE),
         SPAWN_CODE: spawn_effect, FREEZE_CODE: freeze_effect,
         NUKE_CODE: make_nuke(board.remove_node), BURN_CODE: burn_effect,
         POISON_CODE: poison_effect, CAPITAL_CODE: capital_effect,
         RAGE_CODE: make_rage(board.rage)}

