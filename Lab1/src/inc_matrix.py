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

    def convert_to_adj_matrix(self):
        matrix_size = len(self.representation)
        data = [[0 for i in range(matrix_size)] for j in range(matrix_size)]

        for col in range(len(self.representation[0])):
            count = 0
            indexes = []
            for row in range(matrix_size):
                if self.representation[row][col] == 1:
                    indexes.append(row)
                    count += 1
                if count == 2:
                    break
            data[indexes[0]][indexes[1]] = 1
            data[indexes[1]][indexes[0]] = 1

        return adj_matrix.AdjMatrix(data=data)

    def convert_to_inc_matrix(self):
        return self

    def convert_to_adj_list(self):
        data = {}
        key = 1
        n = len(self.representation)

        for i in range(len(self.representation)):
            data[key] = []
            for j in range(len(self.representation[i])):
                if self.representation[i][j] == 1:
                    for k in range(n):
                        if self.representation[k][j] == 1 and k+1 != key:
                            data[key].append(k+1)
                            break
            key += 1

        return adj_list.AdjList(data=data)