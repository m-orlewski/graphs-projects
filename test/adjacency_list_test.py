import sys
sys.path.insert(1, '..')
import unittest
import numpy as np
import adj_list



class AdjListTest(unittest.TestCase):
    def test_load_data(self):
        adjlist = adj_list.AdjList('../adj_list.txt')
        matrixdata = [[2,5,6],
                        [1,3,6],
                        [2,4,5,12],
                        [3,8,9,11],
                        [1,3,7,9],
                        [1,2,7],
                        [5,6,8],
                        [4,7,9,12],
                        [4,5,8,10],
                        [9],
                        [4],
                        [3,8]]
        self.assertListEqual(adjlist.representation, matrixdata)

    def test_convert_to_adj_matrix(self):
        adjlist = adj_list.AdjList('../adj_list.txt')
        matrixdata =   [[0,1,0,0,1,1,0,0,0,0,0,0],
                        [1,0,1,0,0,1,0,0,0,0,0,0],
                        [0,1,0,1,1,0,0,0,0,0,0,1],
                        [0,0,1,0,0,0,0,1,1,0,1,0],
                        [1,0,1,0,0,0,1,0,1,0,0,0],
                        [1,1,0,0,0,0,1,0,0,0,0,0],
                        [0,0,0,0,1,1,0,1,0,0,0,0],
                        [0,0,0,1,0,0,1,0,1,0,0,1],
                        [0,0,0,1,1,0,0,1,0,1,0,0],
                        [0,0,0,0,0,0,0,0,1,0,0,0],
                        [0,0,0,1,0,0,0,0,0,0,0,0],
                        [0,0,1,0,0,0,0,1,0,0,0,0]]
        obj = adjlist.convert_to_adj_matrix()
        self.assertTrue(np.array_equal(obj.representation, matrixdata, equal_nan = True))


    def test_convert_to_inc_matrix(self):
        adjlist = adj_list.AdjList('../adj_list.txt')
        matrixdata =   [[1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,1,0,1,1,1,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,1,0,0,1,1,1,0,0,0,0,0,0,0],
                        [0,1,0,0,0,0,1,0,0,0,0,1,1,0,0,0,0,0],
                        [0,0,1,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,1,0,1,1,0,0,0],
                        [0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,1,1,0],
                        [0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,1,0,1],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                        [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0]]
        obj = adjlist.convert_to_inc_matrix()
        self.assertListEqual(obj.representation, matrixdata)
        
if __name__ == '__main__':
    unittest.main()