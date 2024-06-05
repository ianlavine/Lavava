from typing import Any, Union, Tuple, get_type_hints
import pygame as py
from constants import BURN_CODE, CAPITAL_CODE, EVENT_CODES, RAGE_CODE, PORT_COUNT, SPAWN_CODE, FREEZE_CODE, ZOMBIE_CODE, NUKE_CODE, CANNON_SHOT_CODE, BRIDGE_CODE, CANNON_CODE, STANDARD_LEFT_CLICK, RESTART_GAME_VAL
from highlight import Highlight
from constants import ABILITIES_SELECTED, EDGE_CODE, SPAWN_CODE, STANDARD_RIGHT_CLICK, OVERRIDE_RESTART_CODE, RESTART_CODE, FORFEIT_CODE
from drawClasses import EventVisual, Node, Edge, OtherPlayer, MyPlayer, ReloadAbility, IDItem, State, Event
from angled_position import angles
from chooseUI import ChooseReloadUI
from draw2 import Draw2
from state_dictionary import state_dict
from SettingsUI import settings_ui
from temp_network import Network
from default_abilities import VISUALS, CLICKS, EVENTS
from default_colors import PLAYER_COLORS
from abilityManager import AbstractAbilityManager
from ability_validators import make_ability_validators, unowned_node, make_event_validators
from playerStateEnums import PlayerStateEnum as PSE
from clickTypeEnum import ClickType
from collections import defaultdict
import sys
import math

class SafeNestedDict(dict):
    def __getitem__(self, key):
        if key in self:
            # Directly access the dictionary to avoid recursion
            nested_dict = dict.__getitem__(self, key)
            return lambda k: nested_dict[k]
        else:
            # If the key doesn't exist, return a function that just returns the key it was given
            return lambda k: k

def get_adjusted_type_hints(obj):
    hints = get_type_hints(obj)
    adjusted_hints = {}

    for name, type_hint in hints.items():
        # Check if this is an Optional or Union type with NoneType as one of the options
        if hasattr(type_hint, '__origin__') and type_hint.__origin__ is Union and type(None) in type_hint.__args__:
            # Assume there's exactly one non-NoneType, use it directly
            adjusted_hints[name] = next(t for t in type_hint.__args__ if t is not type(None))
        else:
            adjusted_hints[name] = type_hint

    return adjusted_hints

class Main:

    def __init__(self):
        py.init() 

        self.ps = PSE.ABILITY_SELECTION.value
        self.timer = 60
        self.highlight = Highlight()
        self.effect_visuals = defaultdict(dict)

        self.drawer = Draw2(self.highlight, self.effect_visuals)
        self.can_draw = False

        data, port = self.settings()
        abilities = {BRIDGE_CODE: 2, CANNON_CODE: 2, CAPITAL_CODE: 2}
        self.network = Network(self.setup, self.update, data, abilities, port)
        self.network.receive_board_data()

        self.run()

    def setup(self, start_data):
        pi = start_data["player_id"]
        pc = start_data["player_count"]
        n, e = start_data["board"]["nodes"], start_data["board"]["edges"]
        abi, credits = start_data["abilities"]['values'], start_data["abilities"]['credits']

        self.my_player = MyPlayer(str(pi), PLAYER_COLORS[pi])
        self.players = {id: OtherPlayer(str(id), PLAYER_COLORS[id]) for id in range(pc) if id != pi} | {pi: self.my_player}
        self.nodes = {id: Node(id, ClickType.NODE, n[id]["pos"], n[id]["is_port"], *self.make_ports(n[id]["is_port"]), state_dict[n[id]["state"]], n[id]['value']) for id in n}
        self.edges = {id: Edge(id, ClickType.EDGE, self.nodes[e[id]["from_node"]], self.nodes[e[id]["to_node"]], e[id]["dynamic"]) for id in e}

        self.types = SafeNestedDict({OtherPlayer: self.players, Node: self.nodes, Edge: self.edges, State: state_dict})

        chosen_boxes = self.choose_abilities(abi, credits)
        ev = make_event_validators(self.my_player)
        events = {eb: Event(VISUALS[eb], *(EVENTS[eb]), ev[eb]) for eb in EVENT_CODES}
        self.ability_manager = AbstractAbilityManager(chosen_boxes, events)

        self.drawer.set_data(self.my_player, self.players, self.nodes.values(), self.edges.values(), self.ability_manager)
        self.can_draw = True

    def settings(self):
        return settings_ui()
    
    def make_ports(self, is_port):
        if is_port:
            return 1, angles(PORT_COUNT)
        return 0, []
    
    def update(self, update_data):

        self.ps = update_data['player']['ps']
        self.timer = update_data['countdown_timer']

        self.parse(self.ability_manager.abilities, update_data['player']['abilities'])
        self.parse(self.nodes, update_data['board']['nodes'])
        self.parse(self.edges, update_data['board']['edges'])


    def parse(self, items: dict[int, Any], updates, most_complex_item=None):

        try:
            # deleted_items = set(items) - set(updates)
            
            # for d in deleted_items:
            #     items.pop(d)

            new_items = set(updates) - set(items)
            if new_items:
                new_edges = {id: Edge(id, ClickType.EDGE, self.nodes[updates[id]["from_node"]], self.nodes[updates[id]["to_node"]], updates[id]["dynamic"]) for id in new_items}
                self.edges.update(new_edges)

            if most_complex_item is None:
                # select an arbitrary item to get the type hints
                most_complex_item = next(iter(items.values()))

            i_t = get_adjusted_type_hints(type(most_complex_item))
            # update_types = {key: self.types[i_t[key]] for key in updates[0] if not is_prim(i_t[key])}
            for u in updates:
                obj = items[u]

                if updates[u] == "Deleted":
                    items.pop(u)
                    continue

                for key, val in updates[u].items():
                    if hasattr(obj, key):

                        update_val = val

                        if update_val is not None:

                            desired_type = i_t[key]
                            update_val = self.types[desired_type](val)
                                
                        setattr(obj, key, update_val)

                    else:
                        print(f"key {key} not in {type(obj)}")

        except Exception as e:
            print(e)
            print('items')
            print(items)
            print("UPDATES")
            print(updates)
            sys.exit()

    def print_dict(self, items, indent):
        for key, value in items.items():
            if isinstance(value, dict):
                print(f"{' ' * indent}{key}:")
                self.print_dict(value, indent + 4)
            else:
                print(f"{' ' * indent}{key}: {value}")

    def send_abilities(self, boxes):
        self.chosen_abilities = {ab: boxes[ab].remaining for ab in boxes}
        self.network.send({'code': ABILITIES_SELECTED} | {'body': self.chosen_abilities})

    def choose_abilities(self, abi, credits):
        av = make_ability_validators(self.my_player, self.nodes, self.edges)
        boxes = {ab: ReloadAbility(VISUALS[ab], *(CLICKS[ab]), av[ab], abi[ab]['credits'], abi[ab]['reload']) for ab in abi}
        for box in boxes.values():
            if box.visual.color[0] is None:
                box.visual.color = self.my_player.color
        boxes[BRIDGE_CODE].remaining = 2
        boxes[CANNON_CODE].remaining = 2
        boxes[CAPITAL_CODE].remaining = 2
        return {b: v for b, v in boxes.items() if v.remaining > 0}

    def valid_hover(self, position) -> Union[Tuple[IDItem, int], bool]:
        if node := self.find_node(position):
            if self.ps == PSE.START_SELECTION.value:
                if unowned_node([node]):
                    return node, SPAWN_CODE
            elif self.ps == PSE.PLAY.value:
                return self.ability_manager.validate(node)
                
        elif edge := self.find_edge(position):
            if self.ps == PSE.PLAY.value:
                return self.ability_manager.validate(edge)
                
        return False
    
    def find_node(self, position):
        for node in self.nodes.values():
            if (
                (position[0] - node.pos[0]) ** 2 + (position[1] - node.pos[1]) ** 2
            ) <= (node.size) ** 2 + 3:
                return node
        return None

    def find_edge(self, position):

        def distance_point_to_segment(px, py, x1, y1, x2, y2):
            segment_length_sq = (x2 - x1) ** 2 + (y2 - y1) ** 2

            if segment_length_sq < 1e-6:
                return math.sqrt((px - x1) ** 2 + (py - y1) ** 2)

            t = max(
                0, min(1, ((px - x1) * (x2 - x1) + (py - y1) * (y2 - y1)) / segment_length_sq)
            )

            closest_x = x1 + t * (x2 - x1)
            closest_y = y1 + t * (y2 - y1)

            distance = math.sqrt((px - closest_x) ** 2 + (py - closest_y) ** 2)
            return distance

        for edge in self.edges.values():
            if (
                distance_point_to_segment(
                    position[0],
                    position[1],
                    edge.from_node.pos[0],
                    edge.from_node.pos[1],
                    edge.to_node.pos[0],
                    edge.to_node.pos[1],
                )
                < 5
            ):
                return edge
        return None
    
    def  mouse_button_down_event(self, button):
        if self.highlight:
            if self.ps == PSE.START_SELECTION.value:
                self.network.send(self.highlight.send_format())
            else:
                if self.ability_manager.use_ability(self.highlight):
                    if data := self.ability_manager.complete_ability():
                        self.network.send(self.highlight.send_format(data))
                elif (event_data := self.ability_manager.use_event(self.highlight)):
                    if button == STANDARD_RIGHT_CLICK and self.highlight.usage == STANDARD_LEFT_CLICK:
                        self.network.send(self.highlight.send_format(event_data, STANDARD_RIGHT_CLICK))
                    else:
                        self.network.send(self.highlight.send_format(event_data))

    def keydown(self, event):
        if event.key == OVERRIDE_RESTART_CODE:
            self.network.simple_send(RESTART_GAME_VAL)
        elif self.ps == PSE.VICTORY.value:
            if event.key == RESTART_CODE:
                self.network.simple_send(RESTART_GAME_VAL)
        elif self.ps == PSE.PLAY.value:
            if event.key in self.ability_manager.abilities:
                if self.ability_manager.select(event.key):
                    self.network.simple_send(event.key)
            elif event.key == FORFEIT_CODE:
                self.network.simple_send(FORFEIT_CODE)
        else:
            print("not playing")

    def run(self):
        while True:
            for event in py.event.get():
                if event.type == py.QUIT:
                    py.quit()
                    return
                elif event.type == py.VIDEORESIZE:
                    self.drawer.relocate(event.w, event.h)
                elif event.type == py.MOUSEMOTION:
                    if hover_result := self.valid_hover(event.pos):
                        self.highlight(*hover_result) 
                    else:
                        self.highlight.wipe()
                elif event.type == py.MOUSEBUTTONDOWN:
                    self.mouse_button_down_event(event.button)
                elif event.type == py.KEYDOWN:
                    self.keydown(event)
            if self.can_draw:
                self.drawer.blit(self.ps, self.timer)
                py.display.flip()


class TestMain(Main):

    def settings(self):
        return ["HOST", 1, 2], str(self.get_local_ip())

    def choose_abilities(self, abi, credits):
        av = make_ability_validators(self.my_player, self.nodes, self.edges)
        counts = {BRIDGE_CODE: 2, CANNON_CODE: 2, CAPITAL_CODE: 2}
        return {ab: ReloadAbility(VISUALS[ab], *(CLICKS[ab]), av[ab], abi[ab]['credits'], abi[ab]['reload'], counts[ab]) for ab in counts}

    def get_local_ip(self):
        import socket
        try:
            # Create a socket connection to determine the local IP address
            # The address '8.8.8.8' and port 80 are used here as an example and do not need to be reachable
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                local_ip = s.getsockname()[0]
            return local_ip
        except Exception as e:
            print(f"Error getting local IP address: {e}")
            return None



if __name__ == "__main__":
   Main()