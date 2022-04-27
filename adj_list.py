import os
import graph_representation as gr
import numpy as np
import adj_matrix
import inc_matrix
class AdjList(gr.GraphRepresentation):
    def __init__(self, filepath):
        data = []
        data2 = []
        super().__init__(filepath)
        with open(filepath, 'r') as file:
            data = file.readlines()[1:]
        for item in data:
            data2.append(list(map(int,item.split())))
        self.representation = data2

    
    def convert_to_adj_matrix(self):
        string = '2\n'
        col_num = max(map(lambda x: x[-1],self.representation))
        data = np.zeros((col_num, col_num), dtype = int)
        for row in range(col_num):
            for index in self.representation[row]:
                data[index-1][row] = 1
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
        string = '1\n'
        row_num = max(map(lambda x: x[-1],self.representation))
        col_num = sum([len(element) for element in self.representation])//2
        data = np.zeros((row_num, col_num), dtype = int)
        col = 0
        for row in self.representation:
            for elem in row:
                if elem > self.representation.index(row):
                    data[elem - 1][col] = 1 
                    data[self.representation.index(row)][col] = 1
                    col += 1                                
        for row in data:
            for col in row:
                string += str(col) + ' '
            string += '\n'
        string = string.replace(' \n', '\n')
        string = string[:string.rfind('\n')]
        with open('temp.txt', 'w+') as f:
            f.write(string)
        obj = inc_matrix.IncMatrix('temp.txt')
        return obj


    def convert_to_adj_list(self):
        return self