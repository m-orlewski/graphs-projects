import unittest
from src.adj_list import AdjList

class AdjListTest(unittest.TestCase):
    def setUp(self):
        self.adj_list = AdjList('../data/adj_list.dat')

    def test_load_data(self):
        expected = {1: [2, 5, 6], 2: [1, 3, 6], 3: [2, 4, 5, 12], 4: [3, 8, 9, 11], 5: [1, 3, 7, 9], 6: [1, 2, 7],
                    7: [5, 6, 8], 8: [4, 7, 9, 12], 9: [4, 5, 8, 10], 10: [9], 11: [4], 12: [3, 8]}
        self.assertDictEqual(self.adj_list.representation, expected)

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
        obj = self.adj_list.convert_to_adj_matrix()
        self.assertListEqual(obj.representation, expected)

    def test_convert_to_inc_matrix(self):
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
        obj = self.adj_list.convert_to_inc_matrix()
        self.assertListEqual(obj.representation, expected)
        
if __name__ == '__main__':
    unittest.main()