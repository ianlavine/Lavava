import numpy as np
import random
from collections import defaultdict
from node import Node
from edge import Edge
from player import Player
 

NODE_COUNT = 80

EDGE_COUNT = 100

SCREEN_WIDTH = 1000

SCREEN_HEIGHT = 1000


nodes = []
edges = []
edgeDict = defaultdict(set)
 



####################

 

#####################

 

def orientation(p, q, r):

    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])

    if val == 0:

        return 0  # Collinear

    return 1 if val > 0 else 2  # Clockwise or Counterclockwise

 

def on_segment(p, q, r):

    return (q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and

            q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1]))

 

def do_intersect(p1, q1, p2, q2):

    o1 = orientation(p1, q1, p2)

    o2 = orientation(p1, q1, q2)

    o3 = orientation(p2, q2, p1)

    o4 = orientation(p2, q2, q1)

 

    if o1 != o2 and o3 != o4:

        return True

 

    if o1 == 0 and on_segment(p1, p2, q1):

        return True

 

    if o2 == 0 and on_segment(p1, q2, q1):

        return True

 

    if o3 == 0 and on_segment(p2, p1, q2):

        return True

 

    if o4 == 0 and on_segment(p2, q1, q2):

        return True

 

    return False

 

def overlap(edge1,edge2):

    return do_intersect(nodes[edge1[0]].pos,nodes[edge1[1]].pos,nodes[edge2[0]].pos,nodes[edge2[1]].pos)

   

 

def check_all_overlaps(edge):

    for key in edgeDict:

        for val in edgeDict[key]:

            if edge[0]!=val and edge[0]!=key and edge[1]!=val and edge[1]!=key:

                if overlap(edge, (key, val)):

                    return False

    return True

 

def nearby(edge):

    return np.sqrt((nodes[edge[0]].pos[0]-nodes[edge[1]].pos[0])**2+(nodes[edge[0]].pos[1]-nodes[edge[1]].pos[1])**2) < 6 * min(SCREEN_WIDTH, SCREEN_HEIGHT)/(NODE_COUNT/1.5)

def make_nodes():  #assumes global list nodes is empty
    count = 0
    while count < NODE_COUNT:
        
        spot = [random.randint(int(SCREEN_WIDTH/10),int(9*SCREEN_WIDTH/10)),random.randint(int(SCREEN_HEIGHT/10),int(9*SCREEN_HEIGHT/10))]

        works=True

        for node in nodes:

            if np.sqrt((spot[0]-node.pos[0])**2+(spot[1]-node.pos[1])**2) < 3*min(SCREEN_WIDTH, SCREEN_HEIGHT)/(NODE_COUNT/1.5):

                works=False

        if works:
            nodes.append(Node(count, spot))
            count += 1

def make_edges():   #assumes global list edges is empty

    edge_set = set()

    count = 0

    while count < EDGE_COUNT:

        num1 = random.randint(0, NODE_COUNT-1)
        num2 = random.randint(0, NODE_COUNT-1)

        while num2 == num1:

            num2 = random.randint(0, NODE_COUNT-1)
 

        combo = (min(num1, num2), max(num1, num2))

        if combo not in edge_set and nearby(combo) and check_all_overlaps(combo):

            edge_set.add(combo)
            edgeDict[num1].add(num2)
            edgeDict[num2].add(num1)
            edges.append(Edge(nodes[num1], nodes[num2]))

            count += 1

    return edges

def remove_excess_nodes():
    return [node for node in nodes if len(node.incoming) + len(node.outgoing) > 0]

##########################



def board():

    make_nodes()
    make_edges()
    nodes = remove_excess_nodes()
    player = Player((255,0,0))
    return nodes, edges, player


running=True


# while running:

#     for event in p.event.get():

#         if event.type == p.QUIT:

#             running= False

#         elif event.type == p.MOUSEBUTTONDOWN:
#             nodes = [] #reset
#             edges = [] #reset
#             edge_set = set()

#             edgeDict = defaultdict(set)
#             position=event.pos
#             screen.fill(WHITE)
#             make_nodes()
#             make_edges()
#             remove_excess_nodes()
#             blit_edges()
#             blit_nodes()

#             # call click on the node which is in the range

#     p.display.update()