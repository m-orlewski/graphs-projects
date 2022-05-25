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
    
    def __str__(self):
        result = ''
        for line in self.representation:
            result+=str(line)
            result+="\n"
        return result.replace('[', ' ').replace(']', ' ')

    def convert_to_adj_matrix(self):
        return self

    def convert_to_inc_matrix(self):
        edges = 0 # ilość krawędzi grafu
        for row in range(len(self.representation)):
            edges += sum(self.representation[row])
        edges //= 2

        length = len(self.representation) # liczba wierzchołków grafu

        data = [[0 for _ in range(int(edges))] for _ in range(length)]
        edge = 0
        for i in range(length):
            for j in range(length):
                if self.representation[i][j] == 1 and i < j: # każdą krawędź dodajemy tylko raz
                    data[i][edge] = 1
                    data[j][edge] = 1
                    edge += 1 # przechodzimy do następnej krawędzi (kolumny macierzy)

        return inc_matrix.IncMatrix(data=data)

    def convert_to_adj_list(self):
        data = {}

        for row in range(len(self.representation)):
            data[row+1] = [] # dodajemy węzeł (numer wiersza) i pustą listę sąsiadów
            for col in range(len(self.representation[0])):
                if self.representation[row][col] == 1:
                    data[row+1].append(col+1) # dodajemy węzeł(numer kolumny) do listy sąsiadów

        return adj_list.AdjList(data=data)