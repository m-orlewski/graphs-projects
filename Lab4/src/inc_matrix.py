from src import adj_matrix
from src import adj_list

class IncMatrix():

    def __init__(self, filepath=None, data=None):

        self.representation = []

        if filepath:
            with open(filepath, 'r') as file:
                for line in file.readlines()[1:]:
                    self.representation.append(list(map(int, line.split())))
        elif data:
            self.representation = data

    def __str__(self):
        result = ''
        for line in self.representation:
            result+=str(line)
            result+="\n"
        return result.replace('[', ' ').replace(']', ' ')

    def convert_to_adj_matrix(self):
        n = len(self.representation) # ilość węzłów grafu
        data = [[0 for _ in range(n)] for _ in range(n)]

        pair = []
        for i in range(len(self.representation[0])):
            for j in range(n):
                if self.representation[j][i] == 1:
                    pair.append(j) # zapisujemy wierzchołki krawędzi
                    if len(pair) == 2:
                        break
            data[pair[0]][pair[1]] = 1 # wpisujemy wierzchołki krawędzi jako sąsiadów w macierzy sąsiedztwa
            data[pair[1]][pair[0]] = 1
            pair = []

        return adj_matrix.AdjMatrix(data=data)

    def convert_to_inc_matrix(self):
        return self

    def convert_to_adj_list(self):
        data = {}
        key = 1
        n = len(self.representation)

        for i in range(len(self.representation)):
            data[i+1] = [] # wpisujemy węzeł i+1 i pustą listę jego sąsiadów
            for j in range(len(self.representation[i])):
                if self.representation[i][j] == 1: # węzeł i+1 jest wierzchołkiem j-tej krawędzi
                    for k in range(n): # szukamy drugiego wierzchołka j-tej krawędzi
                        if self.representation[k][j] == 1 and k+1 != i+1: # węzeł k+1 jest drugim wierzchołkiem j-tej krawędzi
                            data[key].append(k+1)
                            break
            key += 1

        return adj_list.AdjList(data=data)