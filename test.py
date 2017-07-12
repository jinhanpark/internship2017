from my_tokenizer import Tokens
from tree_generator import *
import unittest
#import sys
#sys.setrecursionlimit(10000)

class TestSimplification(unittest.TestCase):

    def simple(self):

        lst = [['2*3', '6.00'],
               ['2*3*-4', '-24.00'],
               ['2*x*3', '6.00*pow(x, 1)']
        ]
        for pair in lst:
            self.assertEqual(str(get_simple_expr(pair[0])), pair[1])



def test(cls):
    suite = unittest.TestLoader().loadTestsFromTestCase(cls)
    unittest.TextTestRunner(verbosity=2).run(suite)


def main():
    test(TestSimplification)

main()
