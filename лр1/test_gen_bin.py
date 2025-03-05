import unittest
from gen_bin import gen_bin_tree

class TestGenBinTree(unittest.TestCase):

    def test_height_zero(self):
        tree = gen_bin_tree(root=4, height=0)
        self.assertEqual(tree, {4: []})

    def test_height_one(self):
        tree = gen_bin_tree(root=4, height=1)
        self.assertEqual(tree, {4: [8, 7]})

    def test_height_2(self):
        tree = gen_bin_tree(root=3, height=2)
        expected_tree = {3: [6, 6], 6: [12, 9]}
        self.assertEqual(tree, expected_tree)


if __name__ == '__main__':
    unittest.main()