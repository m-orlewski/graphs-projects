import graph_representation as gr
import numpy as np
import adj_list
import inc_matrix


class AdjMatrix(gr.GraphRepresentation):
    def __init__(self, filepath):
        data = []
        try:
            with open(filepath, 'r') as file:
                super().__init__(filepath)
                data = file.readlines()[1:]
        except:
            print(f"Could not find: {filepath}")
        self.representation = np.loadtxt(data)
    
    def convert_to_adj_matrix(self):
        return self

    def convert_to_inc_matrix(self):
        string = ''
        string += '1\n'
        edges = int(np.sum(self.representation == 1)/2)
        length = int(len(self.representation))
        edge_num = 0
        row_num = 0
        data = np.zeros((length, edges), dtype=int)
        for row in self.representation:
            col_num = 0
            for col in row:
                if col == 1 and col_num > row_num:
                    data[row_num][edge_num] = 1
                    data[col_num][edge_num] = 1
                    edge_num += 1
                col_num += 1
            row_num += 1
        for row in data:
            for col in row:
                string += str(col) + ' '
            string += '\n'
        string = string.replace(' \n', '\n')
        string = string[:string.rfind('\n')]
        with open('temp1.txt', 'w+') as f:
            f.write(string)
        obj = inc_matrix.IncMatrix('temp1.txt')
        return obj

    def convert_to_adj_list(self):
        string = ''
        string += '2\n'
        for row in self.representation:
            col_num = 1
            for col in row:
                if col == 1:
                    string += str(col_num) + ' '
                col_num += 1
            string += '\n'
        string = string.replace(' \n', '\n')
        string = string[:string.rfind('\n')]
        with open('temp.txt', 'w+') as f:
            f.write(string)
        obj = adj_list.AdjList('temp.txt')
        return obj