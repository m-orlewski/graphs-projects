from src import adj_matrix
from src import inc_matrix

class AdjList():

    def __init__(self, filepath=None, data=None):

        self.representation = {}

        if filepath:
            with open(filepath, 'r') as file:
                key = 1
                for line in file.readlines()[1:]:
                    self.representation[key] = []
                    for l in line.strip().split():
                        self.representation[key].append(int(l))
                    key += 1
        elif data:
            self.representation = data
    
    def convert_to_adj_matrix(self):
        n = 0
        for value in self.representation.values():
            if max(value) > n:
                n = max(value)

        data = [[0 for _ in range(n)] for _ in range(n)]

        for key, value in self.representation.items():
            for elem in value:
                data[key - 1][elem - 1] = 1

        return adj_matrix.AdjMatrix(data=data)
        

    def convert_to_inc_matrix(self):
        n = 0
        edges = 0
        for value in self.representation.values():
            edges += len(value)
            if max(value) > n:
                n = max(value)

        edges //= 2
        data = [[0 for _ in range(edges)] for _ in range(n)]

        edge = 0
        for key, value in self.representation.items():
            for elem in value:
                if key < elem:
                    data[key - 1][edge] = 1
                    data[elem - 1][edge] = 1
                    edge += 1

        return inc_matrix.IncMatrix(data=data)


    def convert_to_adj_list(self):
        return self