import math
import pygame as py
from constants import *

class Draw:
    def __init__(self, board, ability_manager, player_manager):
        self.set_data(board, ability_manager, player_manager)
        self.screen = py.display.set_mode(size, py.RESIZABLE)
        self.font = py.font.Font(None, 60)
        self.small_font = py.font.Font(None, 45)
        self.smaller_font = py.font.Font(None, 35)
        self.temp_line = None
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT

        py.display.set_caption("Lavava")

    def set_data(self, board, ability_manager, player_manager):
        self.board = board
        self.edges = board.edges
        self.nodes = board.nodes
        self.players = [x for x in player_manager.player_dict.values()]
        self.player_manager = player_manager
        self.abilities = ability_manager.abilities
        self.ability_manager = ability_manager

    def _generate_darker_color(self, color):
        return tuple(max(c - 50, 0) for c in color)

    def _generate_lighter_color(self, color):
        return tuple(min(c + 50, 255) for c in color)

    def draw_button(self, shape, color, name, cost, letter, position, selected, loading=False):
        btn_size = ABILITY_SIZE * self.height
        border_thickness = 5

        if selected:
            lighter_color = self._generate_lighter_color(color)
            py.draw.rect(self.screen, lighter_color, 
                        (position[0] - border_thickness, 
                        position[1] - border_thickness, 
                        btn_size + 2 * border_thickness, 
                        btn_size + 2 * border_thickness))

        # Draw the button background
        darker_color = self._generate_darker_color(color)
        py.draw.rect(self.screen, darker_color, (position[0], position[1], btn_size, btn_size))

        # Drawing shapes inside
        lighter_color = self._generate_lighter_color(color)
        if shape == "circle":
            py.draw.circle(self.screen, lighter_color, (position[0] + btn_size // 2, position[1] + btn_size // 2), btn_size // 3)
        elif shape == "square":
            py.draw.rect(self.screen, lighter_color, (position[0] + btn_size // 4, position[1] + btn_size // 4, btn_size // 2, btn_size // 2))
        elif shape == "triangle":
            points = [
                (position[0] + btn_size // 2, position[1] + btn_size // 4),
                (position[0] + btn_size // 4, position[1] + 3 * btn_size // 4),
                (position[0] + 3 * btn_size // 4, position[1] + 3 * btn_size // 4)
            ]
            py.draw.polygon(self.screen, lighter_color, points)
        elif shape == "star":
            self.draw_star((position[0] + btn_size // 2, position[1] + btn_size // 2), btn_size, lighter_color)

        if loading:
            py.draw.rect(self.screen, BLACK, 
                        (position[0], 
                        position[1], 
                        btn_size, 
                        btn_size))

        # Drawing text (name and cost)
        font = py.font.Font(None, int(self.height * ABILITY_FONT))

        letter_text = font.render(letter, True, BLACK)  # White color
        self.screen.blit(letter_text, (position[0] + (btn_size - letter_text.get_width()) // 2, 
                                   position[1] + (btn_size - letter_text.get_height()) // 2))

        text = font.render(name, True, WHITE)
        self.screen.blit(text, (position[0] + (btn_size - text.get_width()) // 2, position[1] + btn_size - (FONT_GAP * self.height)))

        cost_text = font.render(f"{cost}", True, WHITE)
        self.screen.blit(cost_text, (position[0] + 10, position[1] + 10))

    def draw_buttons(self):
        y_position = int(ABILITY_START_HEIGHT * self.height)
        for btn in self.abilities.values():
            btn_box = btn.box
            selected = self.ability_manager.mode == btn.key or (self.ability_manager.mode == 'default' and btn.key == 2)
            loading = False
            if CONTEXT['mode'] == 2:
                if not self.ability_manager.full(btn.key):
                    loading = True
            self.draw_button(btn_box.shape, btn_box.color, btn_box.name, btn_box.display_num, btn_box.letter, (self.width -  int(ABILITY_GAP * self.height), y_position), selected, loading)
            y_position += int(ABILITY_GAP * self.height) # Vertical gap between buttons

    def draw_star(self, position, size, color, filled=True):
        inner_radius = size // 6  
        outer_radius = size // 3  
        star_points = []
        
        for i in range(5):
            angle = math.radians(i * 72 + 55)  # Start at top point
            
            # Outer points
            x = position[0] + outer_radius * math.cos(angle)
            y = position[1] + outer_radius * math.sin(angle)
            star_points.append((x, y))
            
            # Inner points
            angle += math.radians(36)  # Halfway between outer points
            x = position[0] + inner_radius * math.cos(angle)
            y = position[1] + inner_radius * math.sin(angle)
            star_points.append((x, y))

        if filled:
            py.draw.polygon(self.screen, color, star_points)
        else:
            py.draw.lines(self.screen, color, True, star_points)
    
    def edge_highlight(self, dy, dx, magnitude, length_factor, start, end, spacing):
        # Calculate the angle of rotation
        angle = math.degrees(math.atan2(dy, dx))
        
        # Calculate the dimensions of the capsule
        width = magnitude  # Length of the row of triangles
        height = length_factor * 2 + 15  # Height based on the triangle size with some padding
        
        # Create a new surface for the capsule
        capsule_surface = py.Surface((int(width), int(height)), py.SRCALPHA)

        # Calculate starting and ending points for the two lines based on the triangle's spacing
        line_start_x = int(height/2) + spacing
        line_end_x = int(width - height/2) - spacing

        # Draw the lines
        py.draw.line(capsule_surface, self.board.highlighted_color, (line_start_x, 2), (line_end_x, 2), 2)
        py.draw.line(capsule_surface, self.board.highlighted_color, (line_start_x, height - 2), (line_end_x, height - 2), 2)
        
        # Rotate the surface containing the capsule
        rotated_surface = py.transform.rotate(capsule_surface, -angle)  # Negative because Pygame's rotation is counter-clockwise
        
        # Calculate the new position for the rotated surface
        rotated_width, rotated_height = rotated_surface.get_size()
        screen_pos = (start[0] + (end[0] - start[0]) / 2 - rotated_width / 2, start[1] + (end[1] - start[1]) / 2 - rotated_height / 2)
        
        # Blit the rotated surface onto the main screen
        self.screen.blit(rotated_surface, screen_pos)

    def draw_arrow(self, edge, color, start, end, triangle_size=5, spacing=9):
        
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        magnitude = max(math.sqrt(dx*dx + dy*dy), 1)
        
        dx /= magnitude
        dy /= magnitude
        
        num_triangles = int((magnitude-10) / spacing)
        
        length_factor = 1.5
        
        for i in range(1, num_triangles + 1):
            pos = (start[0] + i * spacing * dx +5*dx, start[1] + i * spacing * dy+5*dy)
            
            point1 = pos
            point2 = (pos[0] - length_factor * triangle_size * dx + triangle_size * dy, pos[1] - length_factor * triangle_size * dy - triangle_size * dx)
            point3 = (pos[0] - length_factor * triangle_size * dx - triangle_size * dy, pos[1] - length_factor * triangle_size * dy + triangle_size * dx)

            if edge.flowing:
                if edge.currently_raging:
                    py.draw.polygon(self.screen, PURPLE, [point1, point2, point3])
                else:
                    py.draw.polygon(self.screen, color, [point1, point2, point3])
            else:
                py.draw.lines(self.screen, color, True, [point1, point2, point3])

        if self.board.highlighted == edge:
            self.edge_highlight(dy, dx, magnitude, length_factor, start, end, spacing)

    def draw_circle(self, edge, color, start, end, circle_radius=3, spacing=6):

        length_factor = 1.5
        triangle_size = 7
        
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        magnitude = math.sqrt(dx*dx + dy*dy)
        
        dx /= magnitude
        dy /= magnitude
        
        num_circles = int((magnitude-10) / spacing)
        
        for i in range(1, num_circles):
            pos = (start[0] + i * spacing * dx+5*dx, start[1] + i * spacing * dy+5*dy)
            if edge.flowing:
                if edge.currently_raging:
                    py.draw.circle(self.screen, PURPLE, (int(pos[0]), int(pos[1])), circle_radius)
                else:
                    py.draw.circle(self.screen, color, (int(pos[0]), int(pos[1])), circle_radius)
            else:
                py.draw.circle(self.screen, color, (int(pos[0]), int(pos[1])), circle_radius, 1)

        if self.board.highlighted == edge:
            self.edge_highlight(dy, dx, magnitude, length_factor, start, end, spacing)

        point1 = pos
        point2 = (pos[0] - length_factor * triangle_size * dx + triangle_size * dy, pos[1] - length_factor * triangle_size * dy - triangle_size * dx)
        point3 = (pos[0] - length_factor * triangle_size * dx - triangle_size * dy, pos[1] - length_factor * triangle_size * dy + triangle_size * dx)
        py.draw.polygon(self.screen, (153, 255, 51), [point1, point2, point3])
        py.draw.lines(self.screen, color, True, [point1, point2, point3])               
                
    def blit_edges(self):
        for edge in self.edges:
            if edge.state == 'one-way':
                self.draw_arrow(edge,edge.color,edge.from_node.pos,edge.to_node.pos)         
            else:
                self.draw_circle(edge,edge.color,edge.from_node.pos,edge.to_node.pos)

    def blit_nodes(self):
        for spot in self.nodes:
            if spot.state_name == 'mine':
                state = spot.state
                if spot.owner != None:
                    angle1 = 2 * math.pi * ((state.bubble - spot.value) / state.bubble)
                    py.draw.arc(self.screen, state.color, (spot.pos[0] - spot.size, spot.pos[1] - spot.size, spot.size * 2, spot.size * 2), -angle1 / 2, angle1 / 2, spot.size)
                    py.draw.arc(self.screen, spot.owner.color, (spot.pos[0] - spot.size, spot.pos[1] - spot.size, spot.size * 2, spot.size * 2), angle1 / 2, -angle1 / 2 + 2 * math.pi, spot.size)
                else:
                    py.draw.circle(self.screen, GREY, spot.pos, spot.size)
                py.draw.circle(self.screen, spot.state.ring_color, spot.pos, spot.size + 6, 6)
            else:
                py.draw.circle(self.screen, spot.color, spot.pos, spot.size)
            if spot.state_name == 'poisoned':
                py.draw.circle(self.screen, PURPLE, spot.pos, spot.size + 6, 6)
            if spot.full:
                py.draw.circle(self.screen, BLACK, spot.pos, spot.size + 3, 3)
                if spot.state_name == 'capital':
                    py.draw.circle(self.screen, PINK, spot.pos, spot.size + 6, 4)
            if self.board.highlighted == spot:
                py.draw.circle(self.screen, self.board.highlighted_color, spot.pos, spot.size + 5,3)
            if spot.owner and spot.item_type == PORT_NODE and spot.is_port:
                port_width, port_height = spot.size * 1.5, spot.size / 1.5  # Size of the ports
                port_color = BROWN
                if spot.on_fire:
                    port_color = STRONG_ORANGE
                    percentage = spot.burning / BURN_TIME
                    port_width *= percentage
                port_count = spot.port_count  # Number of ports
                angle_step = 2 * math.pi / port_count  # Angle step for each port

                for i in range(port_count):
                    # Angle for this port
                    angle = i * angle_step
                    # Calculate the center of the port rectangle
                    port_center_x = spot.pos[0] + (spot.size + port_height / 2) * math.cos(angle)
                    port_center_y = spot.pos[1] + (spot.size + port_height / 2) * math.sin(angle)
                    
                    # Create a new surface to draw the port rectangle (with per-pixel alpha)
                    port_surface = py.Surface((port_width, port_height), py.SRCALPHA)
                    py.draw.rect(port_surface, port_color, (0, 0, port_width, port_height))
                    
                    # Rotate the port surface to point outwards
                    rotated_port = py.transform.rotate(port_surface, math.degrees(-angle))

                    # Get the new rect to blit the rotated port
                    rotated_rect = rotated_port.get_rect(center=(port_center_x, port_center_y))

                    # Blit the rotated port surface onto the screen
                    self.screen.blit(rotated_port, rotated_rect.topleft)


                
    def blit_numbers(self):
        py.draw.rect(self.screen,WHITE,(0,0,self.width,self.height/13))
        if CONTEXT['mode'] != 2:
            self.screen.blit(self.font.render(str(int(CONTEXT['main_player'].money)),True,CONTEXT['main_player'].color),(20,20))
            self.screen.blit(self.small_font.render(f"{CONTEXT['main_player'].production_per_second:.0f}", True, (205, 204, 0)), (23, 60))
        for i in range(len(self.players)):
            self.screen.blit(self.small_font.render(str(int(self.players[i].count)),True,self.players[i].color),(self.width/3 + i*150,20))
            if self.players[i].capital_count > 0:
                self.screen.blit(self.smaller_font.render(str(int(self.players[i].capital_count)),True,PINK),(self.width/3 + i*150 + 40,20))
        
        if self.player_manager.victor:
            self.screen.blit(self.font.render(f"Player {self.player_manager.victor.id} Wins!",True,self.player_manager.victor.color),(self.width - 450,20))
            if CONTEXT['main_player'].victory:
                self.screen.blit(self.small_font.render("R to restart",True,CONTEXT['main_player'].color),(self.width - 300,60))
            else:
                self.screen.blit(self.small_font.render(f"Waiting for Player {self.player_manager.victor.id} to restart",True,self.player_manager.victor.color),(self.width - 600,60))
        elif self.player_manager.timer > 0:
            if self.player_manager.timer < 4:
                self.screen.blit(self.font.render(f"{self.player_manager.timer + 1:.0f}",True,BLACK),(self.width - 300,20))
            else:
                self.screen.blit(self.font.render(f"{self.player_manager.timer + 1:.0f}",True,CONTEXT['main_player'].color),(self.width - 300,20))
        elif CONTEXT['main_player'].eliminated:
            self.screen.blit(self.font.render("ELIMINATED",True,CONTEXT['main_player'].color),(self.width - 450,20))
        else:
            self.screen.blit(self.small_font.render("X to Forfeit",True,CONTEXT['main_player'].color),(self.width - 450,20))

    def blit_waiting(self):
        self.screen.blit(self.small_font.render("Waiting for other Players to Choose Abilities",True,GREEN),(self.width // 7,20))

    def wipe(self):
        self.screen.fill(WHITE)
            
    def edge_build(self, end, type):
        if type == 1:
            start=self.abilities[BRIDGE_CODE].clicks[0].pos
        else:
            start=self.abilities[D_BRIDGE_CODE].clicks[0].pos
        triangle_size=5
        spacing=9
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        magnitude = math.sqrt(dx*dx + dy*dy)
        
        dx /= magnitude
        dy /= magnitude
        
        num_shapes = int((magnitude-10) / spacing)
        
        length_factor = 1.5
        
        for i in range(1, num_shapes + 1):
            pos = (start[0] + i * spacing * dx +5*dx, start[1] + i * spacing * dy+5*dy)
            
            if type == 1:
                point1 = pos
                point2 = (pos[0] - length_factor * triangle_size * dx + triangle_size * dy, pos[1] - length_factor * triangle_size * dy - triangle_size * dx)
                point3 = (pos[0] - length_factor * triangle_size * dx - triangle_size * dy, pos[1] - length_factor * triangle_size * dy + triangle_size * dx)
                py.draw.polygon(self.screen, YELLOW, [point1, point2, point3])
                py.draw.lines(self.screen, BLACK, True, [point1, point2, point3]) 
            else:
                py.draw.circle(self.screen, YELLOW, pos, 3)
                py.draw.circle(self.screen, BLACK, (int(pos[0]), int(pos[1])), 3, 1)

    def blit_capital_stars(self):
        for spot in self.nodes:
            if spot.state_name == 'capital' and spot.state.capitalized:
                self.draw_star(spot.pos, spot.size * 2, PINK)
                self.draw_star(spot.pos, spot.size * 2, BLACK, False)

    def blit(self, mouse_pos, waiting=False):
        self.screen.fill(WHITE)
        self.blit_nodes()
        self.blit_edges()
        self.blit_capital_stars()
        if waiting:
            self.blit_waiting()
        else:
            self.blit_numbers()
        self.draw_buttons()
        if BRIDGE_CODE in self.abilities and len(self.abilities[BRIDGE_CODE].clicks) >= 1:
            self.edge_build(mouse_pos, 1)
        if D_BRIDGE_CODE in self.abilities and len(self.abilities[D_BRIDGE_CODE].clicks) >= 1:
            self.edge_build(mouse_pos, 2)
        py.display.update() 

    def relocate(self, width, height):
        self.width = width
        self.height = height

    def close_window(self):
        py.display.quit()
        py.quit()
