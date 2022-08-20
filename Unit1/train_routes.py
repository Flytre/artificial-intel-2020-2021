import heapq
import sys
import time
from math import pi, acos, sin, cos
import tkinter as tk

# setting up: Map ids to names, map ids to coords, and map all possible connections from a node
id_to_name = dict()
name_to_id = dict()
node_coords = dict()
connections = dict()

with open("rrNodeCity.txt") as f:
    for line in f:
        split = line.split()
        name = " ".join(split[1:])
        id_to_name[split[0]] = name
        name_to_id[name] = split[0]
with open("rrNodes.txt") as f:
    for line in f:
        split = line.split()
        node_coords[split[0]] = (float(split[1]), float(split[2]))

with open("rrEdges.txt") as f:
    for line in f:
        split = line.split()
        node1 = split[0]
        node2 = split[1]
        if node1 not in connections:
            connections[node1] = set()
        if node2 not in connections:
            connections[node2] = set()

        connections[node1].add(node2)
        connections[node2].add(node1)


def dijkstra_animated(start_id, end_id):
    closed = set()
    start_val = (0.0, start_id, list())
    fringe = [start_val]
    heapq.heapify(fringe)

    while len(fringe) > 0:
        item = heapq.heappop(fringe)
        if item[1] == end_id:  # if the item being checked is the goal location, return the total distance
            make_green(item)
            return item[0]
        if item[1] not in closed:  # if the location has not already been checked through a shorter route
            closed.add(item[1])
            possibles = connections[item[1]]  # get the possible locations you can move to from a node
            for location in possibles:
                if location not in closed:
                    ancestors = item[2].copy()
                    ancestors.append(item[1])
                    heapq.heappush(fringe, (item[0] + calcd(item[1], location), location, ancestors))
                    # add the location to the to-check
                    make_red(item[1], location)
    return None


def a_star_animated(start_id, end_id):
    closed = set()
    start_val = (0.0, 0.0, start_id, list())  # Format: heuristic, distance, id
    fringe = [start_val]
    heapq.heapify(fringe)

    while len(fringe) > 0:
        item = heapq.heappop(fringe)
        if item[2] == end_id:  # if the item being checked is the goal location, return the total distance
            make_green_astar(item)
            return item[1]
        if item[2] not in closed:  # if the location has not already been checked through a shorter route
            closed.add(item[2])
            possibles = connections[item[2]]  # get the possible locations you can move to from a node
            for location in possibles:
                if location not in closed:
                    current_distance = item[1] + calcd(item[2], location)
                    # Add new location to the heap to check - calculate the heuristic
                    ancestors = item[3].copy()
                    ancestors.append(item[2])
                    heapq.heappush(fringe,
                                   (current_distance + calcd(location, end_id), current_distance, location, ancestors))
                    make_blue(item[2], location)
    return None


def from_name(name1, name2, method):
    id1 = name_to_id[name1]
    id2 = name_to_id[name2]
    return method(id1, id2)


def calcd(id1, id2):
    # y1 = lat1, x1 = long1
    # y2 = lat2, x2 = long2
    # all assumed to be in decimal degrees
    y1, x1 = node_coords[id1]
    y2, x2 = node_coords[id2]

    R = 3958.76  # miles = 6371 km
    y1 *= pi / 180.0
    x1 *= pi / 180.0
    y2 *= pi / 180.0
    x2 *= pi / 180.0

    # approximate great circle distance with law of cosines
    return acos(sin(y1) * sin(y2) + cos(y1) * cos(y2) * cos(x2 - x1)) * R


def to_x_y(id1):
    lat, long = node_coords[id1]
    y_percent = 1.0 - ((lat - 14.68673) / (60.84682 - 14.68673))
    x_percent = (long - (-130.35722)) / abs(130.35722 - 60.02403)
    return x_percent * 800, y_percent * 800


lines = dict()


def create_lines():
    for key in connections:
        set_of_connections = connections[key]
        for value in set_of_connections:
            x1, y1 = to_x_y(key)
            x2, y2 = to_x_y(value)
            lines[(key, value)] = canvas.create_line([(x1, y1), (x2, y2)], tag='network_line')


frame_ct = list()
frame_ct.append(200)


def make_green(item1):
    nodes = item1[2]
    nodes.append(item1[1])
    for i in range(0, len(nodes) - 1):
        canvas.itemconfig(lines[(nodes[i], nodes[i + 1])], fill="green", width=5)
        canvas.itemconfig(lines[(nodes[i + 1], nodes[i])], fill="green", width=5)
    root.update()


def make_green_astar(item1):
    nodes = item1[3]
    nodes.append(item1[2])
    for i in range(0, len(nodes) - 1):
        canvas.itemconfig(lines[(nodes[i], nodes[i + 1])], fill="green", width=5)
        canvas.itemconfig(lines[(nodes[i + 1], nodes[i])], fill="green", width=5)
    root.update()


def make_red(id1, id2):
    canvas.itemconfig(lines[(id1, id2)], fill="red")
    canvas.itemconfig(lines[(id2, id1)], fill="red")
    frame_ct[0] = frame_ct[0] - 1
    if frame_ct[0] == 0:
        root.update()
        frame_ct[0] = 200


def make_blue(id1, id2):
    canvas.itemconfig(lines[(id1, id2)], fill="blue")
    canvas.itemconfig(lines[(id2, id1)], fill="blue")
    frame_ct[0] = frame_ct[0] - 1
    if frame_ct[0] == 0:
        root.update()
        frame_ct[0] = 100


root = tk.Tk()  # creates the frame

canvas = tk.Canvas(root, height=800, width=800,
                   bg='white')  # creates a canvas widget, which can be used for drawing lines and shapes
create_lines()
canvas.pack(expand=True)  # packing widgets places them on the board

name1, name2 = sys.argv[1], sys.argv[2]
from_name(name1, name2, dijkstra_animated)
time.sleep(4)
from_name(name1, name2, a_star_animated)
root.mainloop()
