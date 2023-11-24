from constants import *
from ability import Ability
from ability_validators import *
from ability_return import *
from powerBox_factory import make_boxes

def make_abilities(board):

    boxes = make_boxes()

    return {
        SPAWN_CODE: Ability(SPAWN_CODE, unowned_node, 1, boxes[SPAWN_CODE]),
        BRIDGE_CODE: Ability(BRIDGE_CODE, new_edge_validator(board.check_new_edge), 2, boxes[BRIDGE_CODE], make_new_edge(board.new_edge_id)),
        D_BRIDGE_CODE: Ability(D_BRIDGE_CODE, new_edge_validator(board.check_new_edge), 2, boxes[D_BRIDGE_CODE], make_new_edge(board.new_edge_id)),
        POISON_CODE: Ability(POISON_CODE, standard_node_attack, 1, boxes[POISON_CODE]),
        NUKE_CODE: Ability(NUKE_CODE, standard_node_attack, 1, boxes[NUKE_CODE]),
        CAPITAL_CODE: Ability(CAPITAL_CODE, capital_logic, 1, boxes[CAPITAL_CODE]),
        BURN_CODE: Ability(BURN_CODE, standard_port_node, 1, boxes[BURN_CODE]),
        FREEZE_CODE: Ability(FREEZE_CODE, dynamic_edge_own_either, 1, boxes[FREEZE_CODE], None, EDGE),
        RAGE_CODE: Ability(RAGE_CODE, no_click, 0, boxes[RAGE_CODE])
    }



# def make_abilities(player, board):

#     boxes = make_boxes(player.default_color)

#     def spawn():
#         return {
#             SPAWN_CODE: Ability(SPAWN_CODE, unowned_node, 1, boxes['SpawnBox'])
#         }

#     def bridge():
#         return {
#             BRIDGE_CODE: Ability(BRIDGE_CODE, new_edge_validator(board.check_new_edge), 2, boxes['BridgeBox'], make_new_edge(board.new_edge_id))
#         }

#     def d_bridge():
#         return {
#             D_BRIDGE_CODE: Ability(D_BRIDGE_CODE, new_edge_validator(board.check_new_edge), 2, boxes['D-BridgeBox'], make_new_edge(board.new_edge_id))
#         }

#     def poison():
#         return {
#             POISON_CODE: Ability(POISON_CODE, standard_node_attack, 1, boxes['PoisonBox'])
#         }

#     def nuke():
#         return {
#             NUKE_CODE: Ability(NUKE_CODE, standard_node_attack, 1, boxes['NukeBox'])
#         }

#     def capital():
#         return {
#             CAPITAL_CODE: Ability(CAPITAL_CODE, capital_logic, 1, boxes['CapitalBox'])
#         }

#     def burn():
#         return {
#             BURN_CODE: Ability(POISON_CODE, standard_port_node, 1, boxes['PoisonBox'])
#         }

#     def freeze():
#         return {
#             FREEZE_CODE: Ability(NUKE_CODE, dynamic_edge_own_either, 1, boxes['NukeBox'])
#         }

#     if CONTEXT['mode'] == 1:
#         return spawn() | bridge() | d_bridge() | poison() | nuke() | capital() | freeze()
#     elif CONTEXT['mode'] == 2:
#         return spawn() | bridge() | d_bridge() | poison() | nuke() | freeze()
#     elif CONTEXT['mode'] == 3:
        # return spawn() | bridge() | d_bridge() | poison() | nuke() | capital() | freeze() | burn()