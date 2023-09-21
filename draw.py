import math
import pygame as py
from dynamicEdge import DynamicEdge
from resourceNode import ResourceNode
from constants import *

class Draw:
    def __init__(self, board, player_num, players):
        self.set_data(board, player_num, players)
        self.screen = py.display.set_mode(size, py.RESIZABLE)
        self.font = py.font.Font(None, 60)
        self.small_font = py.font.Font(None, 45)
        self.highlighted_node = None
        self.temp_line = None

        py.display.set_caption("Lavava")

    def set_data(self, board, player_num, players):
        self.board = board
        self.edges = board.edges
        self.nodes = board.nodes
        self.player = players[player_num]
        self.players = players

    def draw_arrow(self, edge, color, start, end, triangle_size=5, spacing=9):
        
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        magnitude = math.sqrt(dx*dx + dy*dy)
        
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
                py.draw.polygon(self.screen, color, [point1, point2, point3])         
            else:
                py.draw.lines(self.screen, color, True, [point1, point2, point3])

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
                py.draw.circle(self.screen, color, (int(pos[0]), int(pos[1])), circle_radius)
            else:
                py.draw.circle(self.screen, color, (int(pos[0]), int(pos[1])), circle_radius, 1)

        point1 = pos
        point2 = (pos[0] - length_factor * triangle_size * dx + triangle_size * dy, pos[1] - length_factor * triangle_size * dy - triangle_size * dx)
        point3 = (pos[0] - length_factor * triangle_size * dx - triangle_size * dy, pos[1] - length_factor * triangle_size * dy + triangle_size * dx)
        py.draw.polygon(self.screen, (153, 255, 51), [point1, point2, point3])
        py.draw.lines(self.screen, color, True, [point1, point2, point3])               
                
    def blit_edges(self):
        for edge in self.edges:
            if not isinstance(edge, DynamicEdge):
                self.draw_arrow(edge,edge.color,edge.from_node.pos,edge.to_node.pos)         
            else:
                self.draw_circle(edge,edge.color,edge.from_node.pos,edge.to_node.pos)

    def blit_nodes(self):
        for spot in self.nodes:
            if isinstance(spot, ResourceNode):
                if spot.popped:
                    py.draw.circle(self.screen, spot.color, spot.pos, spot.size)
                elif spot.bubble_owner != None:
                    angle1 = 2 * math.pi * (spot.bubble_size / spot.bubble)
                    py.draw.arc(self.screen, spot.color, (spot.pos[0] - spot.size, spot.pos[1] - spot.size, spot.size * 2, spot.size * 2), -angle1 / 2, angle1 / 2, spot.size)
                    py.draw.arc(self.screen, spot.bubble_owner.color, (spot.pos[0] - spot.size, spot.pos[1] - spot.size, spot.size * 2, spot.size * 2), angle1 / 2, -angle1 / 2 + 2 * math.pi, spot.size)
                else:
                    py.draw.circle(self.screen, GREY, spot.pos, spot.size)
                py.draw.circle(self.screen, spot.ring_color, spot.pos, spot.size + 6, 6)
            else:
                py.draw.circle(self.screen, spot.color, spot.pos, spot.size)
            if spot.full:
                py.draw.circle(self.screen, BLACK, spot.pos, spot.size + 3, 3)
                
    def blit_numbers(self):
        py.draw.rect(self.screen,WHITE,(0,0,SCREEN_WIDTH,SCREEN_HEIGHT/13))
        for i in range(self.board.player_count):
            self.screen.blit(self.small_font.render(str(int(self.players[i].count)),True,self.players[i].color),(SCREEN_WIDTH/3 + i*150,20))
        
        if self.board.victor:
            self.screen.blit(self.font.render(f"Player {self.board.victor.id} Wins!",True,self.board.victor.color),(SCREEN_WIDTH - 300,20))
            if self.player.victory:
                self.screen.blit(self.small_font.render("R to restart",True,self.player.color),(SCREEN_WIDTH - 300,60))
            else:
                self.screen.blit(self.small_font.render(f"Waiting for Player {self.board.victor.id} to restart",True,self.board.victor.color),(SCREEN_WIDTH - 450,60))
        elif self.board.timer > 0:
            if self.board.timer < 4:
                self.screen.blit(self.font.render(f"{self.board.timer + 1:.0f}",True,BLACK),(SCREEN_WIDTH - 100,20))
            else:
                self.screen.blit(self.font.render(f"{self.board.timer + 1:.0f}",True,self.player.color),(SCREEN_WIDTH - 100,20))
        elif self.player.eliminated:
            self.screen.blit(self.font.render("ELIMINATED",True,self.player.color),(SCREEN_WIDTH - 300,20))
        else:
            self.screen.blit(self.small_font.render("X to Forfeit",True,self.player.color),(SCREEN_WIDTH - 300,20))

    def wipe(self):
        self.screen.fill(WHITE)

    def highlight_node(self):
        if self.player.highlighted_node is not None:
            py.draw.circle(self.screen, self.player.color, self.player.highlighted_node.pos, self.player.highlighted_node.size + 5,2)

    def blit(self, mouse_pos):
        self.screen.fill(WHITE)
        self.blit_nodes()
        self.blit_edges()
        self.blit_numbers()
        self.highlight_node()
        py.display.update() 