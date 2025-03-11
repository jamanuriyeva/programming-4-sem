import unittest
from lr2 import *


class TestBinaryTrees(unittest.TestCase):
    def setUp(self):
        self.root = 5
        self.height = 3

    def test_gen_bin_tree1_recursive(self):
        """Проверка корректности рекурсивной генерации бинарного дерева"""
        expected_result = {
            5: [
                {10: [{20: [], 23: []}, {30: [], 33: []}]},
                {8: [{16: [], 19: []}, {18: [], 21: []}]  # Исправлено!
                 }]
        }
        result = gen_bin_tree1(self.root, self.height)
        self.assertDictEqual(result, expected_result)

    def test_gen_bin_tree2_iterative(self):
        """Проверка корректности нерекурсивной генерации бинарного дерева"""
        expected_result = {
            5: [10, 8],
            10: [20, 13],
            8: [16, 11],
            20: [],
            13: [],
            16: [],
            11: []
        }
        result = gen_bin_tree2(self.root, self.height)
        self.assertDictEqual(result, expected_result)

    def test_calculate_time(self):
        """Проверка работы функции calculate_time"""
        n = 10
        total_time = calculate_time(n, gen_bin_tree1)
        self.assertIsInstance(total_time, float)
        self.assertGreater(total_time, 0)


if __name__ == '__main__':
    unittest.main()