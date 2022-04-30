from src import adj_list
from src import inc_matrix


class AdjMatrix():

    def __init__(self, filepath=None, data=None):

        self.representation = []

        if filepath:
            with open(filepath, 'r') as file:
                for line in file.readlines()[1:]:
                    self.representation.append(list(map(int, line.split())))
        elif data:
            self.representation = data
    
    def convert_to_adj_matrix(self):
        return self

    def convert_to_inc_matrix(self):
        edges = 0
        for row in range(len(self.representation)):
            edges += sum(self.representation[row])
        edges //= 2
        length = len(self.representation) # liczba wierzchołków
        edge_num = 0
        row_num = 0
        data = [[0 for _ in range(int(edges))] for _ in range(length)]

        for row in self.representation:
            col_num = 0
            for col in row:
                if col == 1 and col_num > row_num:
                    data[row_num][edge_num] = 1
                    data[col_num][edge_num] = 1
                    edge_num += 1
                col_num += 1
            row_num += 1

        return inc_matrix.IncMatrix(data=data)

    def convert_to_adj_list(self):
        data = {}

        for row in range(len(self.representation)):
            data[row+1] = []
            for col in range(len(self.representation[0])):
                if self.representation[row][col] == 1:
                    data[row+1].append(col+1)

        return adj_list.AdjList(data=data)