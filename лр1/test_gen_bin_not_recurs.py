import unittest
from gen_bin_not_recurs import gen_bin_tree


class TestGenBinTree(unittest.TestCase):

    def test_height_zero(self):
        self.assertEqual(gen_bin_tree(1, 0), {1: []})

    def test_height_one(self):
        self.assertEqual(gen_bin_tree(3, 1), {3: [6, 6]})

    def test_height_two(self):
        expected_output = {1: [2, 4], 2: [4, 5], 4: [8, 7]}
        self.assertEqual(gen_bin_tree(1, 2), expected_output)

    def test_height_four(self):
        expected_output = {1: [2, 4], 2: [4, 5], 4: [8, 7], 5: [10, 8], 7: [14, 10], 8: [16, 11]}
        self.assertEqual(gen_bin_tree(1, 3), expected_output)

if __name__ == "__main__":
    unittest.main()