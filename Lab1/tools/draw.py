from platform import node
from src.adj_list import AdjList
from src.adj_matrix import AdjMatrix
from src.inc_matrix import IncMatrix

import tkinter as tk
from math import cos, sin, pi

def create_circle(canvas, x, y, r, outline="black", fill="white", width=2):
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvas.create_oval(x0, y0, x1, y1, outline=outline, fill=fill, width=width)

def draw_graph(canvas, original_graph):
    canvas.delete("all")

    graph = original_graph
    if not isinstance(original_graph, AdjList):
        graph=original_graph.convert_to_adj_list()
    
    node_count = len(graph.representation)
    center_point = (canvas.winfo_width()/2, canvas.winfo_height()/2)
    radius = min(center_point)/1.5

    angle_delta = 2*pi/node_count
    for i in range(1, node_count+1):
        angle = angle_delta*i
        x = center_point[0] + radius*sin(angle)
        y = center_point[1] - radius*cos(angle)

        for neighbour in graph.representation[i]:
            if neighbour <= i:
                continue
            neighbour_angle = angle_delta * neighbour
            neighbour_x = center_point[0] + radius * sin(neighbour_angle)
            neighbour_y = center_point[1] - radius * cos(neighbour_angle)

            canvas.create_line(x, y, neighbour_x, neighbour_y)

        create_circle(canvas, x, y, radius * 0.2)
        canvas.create_text(x, y, text=str(i))

    