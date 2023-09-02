import math
from node import Node
from edge import Edge
from dynamicEdge import DynamicEdge
import re

def distance_point_to_segment(px, py, x1, y1, x2, y2):
    segment_length_sq = (x2 - x1)**2 + (y2 - y1)**2
    
    if segment_length_sq < 1e-6:
        return math.sqrt((px - x1)**2 + (py - y1)**2)
    
    t = max(0, min(1, ((px - x1) * (x2 - x1) + (py - y1) * (y2 - y1)) / segment_length_sq))
    
    closest_x = x1 + t * (x2 - x1)
    closest_y = y1 + t * (y2 - y1)
    
    distance = math.sqrt((px - closest_x)**2 + (py - closest_y)**2)
    return distance

def size_factor(x):
    if x<5:
        return 0
    if x>=200:
        return 1
    return max(min(math.log10(x/10)/2+x/1000+0.15,1),0)

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

def unwrap_board(s):
    node_dict = {}
    num = int(s[0])
    s = s[1:] 

    nodes = []
    node_matches = re.findall(r"Node\((\d+), (-?\d+\.?\d*), (-?\d+\.?\d*)\)", s)
    for match in node_matches:
        id, x, y = int(match[0]), int(match[1]), int(match[2])
        abe = Node(id, (x, y))
        node_dict[id] = abe
        nodes.append(abe)


    edges = []
    edge_matches = re.findall(r"Edge\((\d+), (\d+), (\d+), (True|False)\)", s)
    for match in edge_matches:
        id1, id2, id3 = int(match[0]), int(match[1]), int(match[2])
        if match[3] == "True":
            edges.append(Edge(node_dict[id1], node_dict[id2], id3))
        else:
            edges.append(DynamicEdge(node_dict[id1], node_dict[id2], id3))


    return (num, (2, nodes, edges))