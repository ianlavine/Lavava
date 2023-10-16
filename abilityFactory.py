from ability import *
from constants import *

class AbilityBuilder:

    def __init__(self, board):
        self.abilities = {}
        
        spawn = Spawn(board.player)
        self.abilities[SPAWN_CODE] = spawn

        bridge = Bridge(board.player, board.new_edge_id, board.check_new_edge, board.buy_new_edge)
        self.abilities[BRIDGE_CODE] = bridge

        nuke = Nuke(board.player, board.remove_node)
        self.abilities[NUKE_CODE] = nuke

        poison = Poison(board.player)
        self.abilities[POISON_CODE] = poison

        freeze = Freeze(board.player)
        self.abilities[FREEZE_CODE] = freeze

        capital = Capital(board.player)
        self.abilities[CAPITAL_CODE] = capital