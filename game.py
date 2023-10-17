import pygame as p
from network import Network
from board import Board
from draw import Draw
from map_builder import MapBuilder
from randomGenerator import RandomGenerator
from player import Player
from constants import *
import sys
from abilityManager import AbilityManager
from playerManager import PlayerManager

class Game:
    def __init__(self):
        p.init()

        self.running = True

        self.network = Network(self.action)

        self.player_num = int(self.network.data[0])
        player_count = int(self.network.data[2])

        self.player_manager = PlayerManager(player_count, self.player_num)
        self.player = self.player_manager.main_player

        self.board = Board(self.player)
        self.ability_manager = AbilityManager(self.player, self.board)
        self.generator = RandomGenerator(int(self.network.data[4:]))

        self.start_game()

        self.drawer = Draw(self.board, self.ability_manager, self.player_manager)

        self.main_loop()

    def start_game(self):
        self.player_manager.reset()
        map_builder = MapBuilder(self.generator)
        self.board.reset(map_builder.node_objects, map_builder.edge_objects)
        self.position = None

    def action(self, key, acting_player, data):
        if key == RESTART_GAME_VAL:
            self.start_game()
            self.drawer.set_data(self.board, self.ability_manager, self.player_manager)
        elif key == ELIMINATE_VAL:
            self.player_manager.eliminate(acting_player)
            self.board.eliminate(self.player_manager.player_dict[acting_player])
        elif key == TICK:
            self.tick()
        elif key in self.ability_manager.abilities:
            new_data = (self.board.id_dict[d] if d in self.board.id_dict else d for d in data)
            self.ability_manager.abilities[key].input(self.player_manager.player_dict[acting_player], new_data)
        elif key == STANDARD_LEFT_CLICK or key == STANDARD_RIGHT_CLICK:
            self.board.id_dict[data[0]].click(self.player_manager.player_dict[acting_player], key)


    def tick(self):
        if self.board and not self.player_manager.victor and not self.player_manager.update_timer():
            self.board.update()
            self.player_manager.update()
            self.player_manager.check_over()
            
    def eliminate_send(self):
        self.network.send((ELIMINATE_VAL, self.player_manager.player, 0))

    def restart_send(self):
        self.network.send((RESTART_GAME_VAL, 0, 0))

    def keydown(self, event):
        if event.type == p.KEYDOWN:
            if self.player.victory:
                if event.key == p.K_r:
                    self.restart_send()
            else:
                if event.key in ABILITY_CODES:
                    self.ability_manager.select(event.key)
                elif event.key == p.K_x:
                    self.eliminate_send()

    def main_loop(self):
        while self.running:
            for event in p.event.get():
                if event.type == p.QUIT:
                    self.running = False

                elif event.type == p.VIDEORESIZE:
                    width, height = event.w, event.h
                    for node in self.board.nodes:
                        node.relocate(width, height)
                    self.drawer.relocate(width, height)

                if not self.player.eliminated:
                    self.keydown(event)

                    if not self.player.victory:
                        if event.type == p.MOUSEBUTTONDOWN:
                            self.mouse_button_down_event(event.button)

                        elif event.type == p.MOUSEMOTION:
                            self.position = event.pos
                            self.board.check_highlight(event.pos, self.ability_manager.ability)

            self.drawer.wipe()
            self.drawer.blit(self.position)

        self.network.stop()
        self.drawer.close_window()
        sys.exit()

    def mouse_button_down_event(self, button):
        if self.board.highlighted:
            if (data := self.ability_manager.use_ability(self.board.highlighted, self.board.highlighted_color)) and button != STANDARD_RIGHT_CLICK:
                self.network.send((self.ability_manager.mode, self.player_num, *data))
                self.ability_manager.update_ability()
            elif id := self.board.click_edge():
                self.network.send((button, self.player_num, id))

if __name__ == "__main__":
    Game()
