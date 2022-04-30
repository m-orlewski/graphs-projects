import unittest
from src.inc_matrix import IncMatrix

class IncMatrixTest(unittest.TestCase):

    def setUp(self):
        self.inc_matrix = IncMatrix('../data/inc_matrix.dat')

    def test_load_data(self):
        expected =   [[1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
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
        self.assertListEqual(self.inc_matrix.representation, expected)

    def test_convert_to_adj_matrix(self):
        expected =   [[0,1,0,0,1,1,0,0,0,0,0,0],
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
        
        adj_matrix = self.inc_matrix.convert_to_adj_matrix()
        self.assertListEqual(adj_matrix.representation, expected)


    def test_convert_to_adj_list(self):
        expected = {1: [2, 5, 6], 2: [1, 3, 6], 3: [2, 4, 5, 12], 4: [3, 8, 9, 11], 5: [1, 3, 7, 9], 6: [1, 2, 7],
                    7: [5, 6, 8], 8: [4, 7, 9, 12], 9: [4, 5, 8, 10], 10: [9], 11: [4], 12: [3, 8]}
        adj_list = self.inc_matrix.convert_to_adj_list()
        self.assertDictEqual(adj_list.representation, expected)


if __name__ == '__main__':
    unittest.main()