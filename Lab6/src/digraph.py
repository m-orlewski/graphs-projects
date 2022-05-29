import networkx as nx

from src.adj_list import AdjList
from src.inc_matrix import IncMatrix
from src.adj_matrix import AdjMatrix

class Digraph:
    '''
    Klasa reprezentująca graf skierowany
    '''

    def __init__(self, from_graph=None):
        if not from_graph:
            self.graph = nx.DiGraph()
        else:
            self.graph = from_graph

    def add_vertex(self, vertex):
        self.graph.add_node(vertex)

    def add_vertices(self, vertices):
        self.graph.add_nodes_from(vertices)

    def add_edge(self, vertex1, vertex2):
        self.graph.add_edge(vertex1, vertex2)

    def get_in_edges(self, vertex):
        return self.graph.in_edges(vertex)

    def get_out_edges(self, vertex):
        return self.graph.out_edges(vertex)

    def get_vertices(self):
        return self.graph.nodes()

    def get_edges(self):
        return self.graph.edges()

    def get_edge_weight(self, vertex1, vertex2):
        return self.graph.get_edge_data(vertex1, vertex2)['weight']

    def to_adj_list(self):
        data = {}
        for vertex in self.get_vertices():
            data[vertex] = []
            for edge in self.get_out_edges(vertex):
                data[vertex].append(edge[1]) # do listy sąsiadów węzła vertex dodajemy węzły do których ma krawędź wychodzącą

        return AdjList(data=data)

    def to_inc_matrix(self):
        data = [[0 for _ in range(len(self.get_edges()))] for _ in range(len(self.get_vertices()))]
        
        i = 0
        for edge in self.get_edges():
            data[edge[0]-1][i] = -1 # węzeł startowy krawędzi
            data[edge[1]-1][i] = 1 # węzeł końcowy krawędzi
            i += 1

        return IncMatrix(data=data)     

    def to_adj_matrix(self):
        data = [[0 for _ in range(len(self.get_vertices()))] for _ in range(len(self.get_vertices()))]
        for vertex in self.get_vertices():
            for edge in self.get_in_edges(vertex):
                data[edge[0]-1][vertex-1] = 1 # do macierzy sąsiadów węzła vertex dodajemy węzły z których krawędzie wchodzą do vertex

        return AdjMatrix(data=data)
                

if __name__ == '__main__':
    pass

    

