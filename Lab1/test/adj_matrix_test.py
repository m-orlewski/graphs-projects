import unittest
from src.adj_matrix import AdjMatrix

class AdjMatrixTest(unittest.TestCase):

    def setUp(self):
        self.adj_matrix = AdjMatrix(filepath='../data/adj_matrix.dat')

    def test_load_data(self):
        expected = [[0,1,0,0,1,1,0,0,0,0,0,0],
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
        self.assertListEqual(self.adj_matrix.representation, expected)

    def test_convert_to_adj_list(self):
        expected = {1: [2, 5, 6], 2: [1, 3, 6], 3: [2, 4, 5, 12], 4: [3, 8, 9, 11], 5: [1, 3, 7, 9], 6: [1, 2, 7],
                    7: [5, 6, 8], 8: [4, 7, 9, 12], 9: [4, 5, 8, 10], 10: [9], 11: [4], 12: [3, 8]}

        adj_list = self.adj_matrix.convert_to_adj_list()
        self.assertDictEqual(adj_list.representation, expected)


    def test_convert_to_inc_matrix(self):
        expected = [[1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
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
        inc_matrix = self.adj_matrix.convert_to_inc_matrix()
        self.assertListEqual(inc_matrix.representation, expected)


if __name__ == '__main__':
    unittest.main()