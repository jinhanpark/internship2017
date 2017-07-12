from my_tokenizer import Tokens
from tree_generator import *

import unittest

class TestSimplification(unittest.TestCase):

    def test_numbers(self):
        lst = [['2*3', '6.00'],
               ['2*3*-4', '-24.00'],
               ['2*-3*2', '-12.00'],
               ['3/2*4', '6.00']
        ]
        for pair in lst:
            self.assertEqual(str(get_simple_expr(pair[0])), pair[1])

    def test_single_var(self):
        lst = [['x', 'pow(x, 1)'],
               ['2*x', '2.00*pow(x, 1)'],
               ['x*3', '3.00*pow(x, 1)'],
               ['1/x', 'pow(x, -1)'],
               ['x*y/x', 'pow(y, 1)']
        ]
        for pair in lst:
            self.assertEqual(str(get_simple_expr(pair[0])), pair[1])


def test(cls):
    suite = unittest.TestLoader().loadTestsFromTestCase(cls)
    unittest.TextTestRunner(verbosity=2).run(suite)

def main():
    tests = [TestSimplification]
    for t in tests:
        test(TestSimplification)

main()
