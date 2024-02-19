import pygame as p
from network import Network
from board import Board
from draw import Draw
from map_builder import MapBuilder
from randomGenerator import RandomGenerator
from playerManager import PlayerManager
from constants import (
    CONTEXT,
    RESTART_GAME_VAL,
    ELIMINATE_VAL,
    ABILITIES_CHOSEN_VAL,
    TICK,
    STANDARD_LEFT_CLICK,
    STANDARD_RIGHT_CLICK,
    OVERRIDE_RESTART_CODE,
    RESTART_CODE,
    FORFEIT_CODE,
)
from modeConstants import MODE_ABILITY_MANAGERS, ABILITY_OPTIONS
import sys
from ability_effects import make_ability_effects
import mode


class Game:
    def __init__(self):

        self.running = True
        self.chose_count = 0

        self.setup()

        self.board = Board()

        self.ability_effects = make_ability_effects(self.board)

        self.start_game()

        self.drawer = Draw(self.board, self.ability_manager, self.player_manager)

        self.main_loop()

    def setup(self):

        self.network = Network(self.action)

        player_num = int(self.network.data[0])
        self.pcount = int(self.network.data[2])
        mode.MODE = int(self.network.data[4])
        self.generator = RandomGenerator(int(self.network.data[6:]))

        self.player_manager = PlayerManager(self.pcount, player_num)

    def start_game(self):
        CONTEXT["started"] = False
        self.chose_count = 0
        self.player_manager.reset()
        map_builder = MapBuilder(self.generator)
        map_builder.build()
        self.ability_manager = MODE_ABILITY_MANAGERS[mode.MODE](self.board)
        self.chose_send()
        self.board.reset(map_builder.node_objects, map_builder.edge_objects)
        self.position = None

    def action(self, key, acting_player, data):
        if key == RESTART_GAME_VAL:
            self.start_game()
            self.drawer.set_data(self.board, self.ability_manager, self.player_manager)
        elif key == ELIMINATE_VAL:
            self.player_manager.eliminate(acting_player)
            self.board.eliminate(self.player_manager.player_dict[acting_player])
        elif key == ABILITIES_CHOSEN_VAL:
            self.chose_count += 1
        elif key == TICK:
            if self.chose_count == self.pcount:
                self.tick()
        elif key in self.ability_options:
            new_data = [
                self.board.id_dict[d] if d in self.board.id_dict else d for d in data
            ]
            self.ability_effects[key](
                new_data, self.player_manager.player_dict[acting_player]
            )
        elif key == STANDARD_LEFT_CLICK or key == STANDARD_RIGHT_CLICK:
            self.board.id_dict[data[0]].click(
                self.player_manager.player_dict[acting_player], key
            )
        else:
            print("NOT ALLOWED")

    def tick(self):
        if (
            self.board
            and not self.player_manager.victor
            and not self.player_manager.update_timer()
        ):
            self.board.update()
            self.player_manager.update()
            self.ability_manager.update()
            self.player_manager.check_over()

    def eliminate_send(self):
        self.network.send((ELIMINATE_VAL, CONTEXT["main_player"].id, 0))

    def restart_send(self):
        self.network.send((RESTART_GAME_VAL, 0, 0))

    def chose_send(self):
        self.network.send((ABILITIES_CHOSEN_VAL, 0, 0))

    def keydown(self, event):
        if event.type == p.KEYDOWN:
            if event.key == OVERRIDE_RESTART_CODE:
                self.restart_send()
            elif CONTEXT["main_player"].victory:
                if event.key == RESTART_CODE:
                    self.restart_send()
            else:
                if event.key in self.ability_manager.abilities:
                    if self.ability_manager.select(event.key):
                        self.network.send(
                            (self.ability_manager.mode, CONTEXT["main_player"].id, 0)
                        )
                        self.ability_manager.update_ability()
                elif event.key == FORFEIT_CODE:
                    self.eliminate_send()

    def main_loop(self):
        while self.running:
            if self.chose_count < self.pcount:
                self.drawer.blit(self.position, True)
            else:
                for event in p.event.get():
                    if event.type == p.QUIT:
                        self.running = False

                    elif event.type == p.VIDEORESIZE:
                        width, height = event.w, event.h
                        for node in self.board.nodes:
                            node.relocate(width, height)
                        self.drawer.relocate(width, height)

                    if not CONTEXT["main_player"].eliminated:
                        self.keydown(event)

                        if not CONTEXT["main_player"].victory:
                            if event.type == p.MOUSEBUTTONDOWN:
                                self.mouse_button_down_event(event.button)

                            elif event.type == p.MOUSEMOTION:
                                self.position = event.pos
                                self.board.check_highlight(
                                    event.pos, self.ability_manager
                                )

                self.drawer.wipe()
                self.drawer.blit(self.position)

        self.network.stop()
        self.drawer.close_window()
        sys.exit()

    def mouse_button_down_event(self, button):
        if self.board.highlighted:
            if (
                data := self.ability_manager.use_ability(
                    self.board.highlighted, self.board.highlighted_color
                )
            ) and button != STANDARD_RIGHT_CLICK:
                self.network.send(
                    (self.ability_manager.mode, CONTEXT["main_player"].id, *data)
                )
                self.ability_manager.update_ability()
            elif id := self.board.click_edge():
                self.network.send((button, CONTEXT["main_player"].id, id))

    @property
    def ability_options(self):
        return ABILITY_OPTIONS[mode.MODE]


if __name__ == "__main__":
    Game()