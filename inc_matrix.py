import graph_representation as gr
import numpy as np
import adj_matrix
import adj_list

class IncMatrix(gr.GraphRepresentation):
    def __init__(self, filepath):
        data = []
        data2 = []
        try:
            with open(filepath, 'r') as file:
                data = file.readlines()[1:]
                super().__init__(filepath)
        except:
            print(f"Could not find: {filepath}")
        for item in data:
            data2.append(list(map(int,item.split())))
        self.representation = data2

    def convert_to_adj_matrix(self):
        string = '3\n'
        matrix_size = len(self.representation)
        data = np.zeros((matrix_size, matrix_size), dtype = int)
        for col in range(len(self.representation[1])):
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
        for row in data:
            for col in row:
                string += str(col) + ' '
            string += '\n'
        string = string.replace(' \n', '\n')
        string = string[:string.rfind('\n')]
        with open('temp1.txt', 'w+') as f:
            f.write(string)
        obj = adj_matrix.AdjMatrix('temp1.txt')
        return obj

    def convert_to_inc_matrix(self):
        return self

    def convert_to_adj_list(self):
        string = '2\n'
        d = {}
        matrix_size = len(self.representation)
        result = []
        for col in range(len(self.representation[1])):
            count = 0
            indexes = []
            for row in range(matrix_size):
                if self.representation[row][col] == 1:
                    indexes.append(row)
                    count += 1
                if count == 2:
                    result.append(indexes)
                    rIndexes = indexes.copy()
                    rIndexes.reverse()
                    result.append(rIndexes) if rIndexes not in result else result
                    break
        for key, value in result:
            if key not in d.keys():
                d[key] = [key]
            d[key].append(value + 1)
        data = list(d.values())
        data.sort()
        for row in data:
            for col in row[1:]:
                string += str(col) + ' '
            string += '\n'
        string = string.replace(' \n', '\n')
        string = string[:string.rfind('\n')]
        with open('temp.txt', 'w+') as f:
            f.write(string)
        obj = adj_list.AdjList('temp.txt')
        return obj