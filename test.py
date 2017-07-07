from my_tokenizer import Tokens
from tree_generator import *
from simplifier import *
import unittest
#import sys
#sys.setrecursionlimit(10000)

def get_simplified_expr_from_string(s):
    tokens = Tokens(s)
    expr = get_expr(tokens)
    expr.simplify()
    return str(expr)

class TestSimplification(unittest.TestCase):

    def test_get_coeff(self):

        lst = [['2*3', '6.00'],
               ['2*3*4', '24.00'],
               ['2*x*3', '6.00*pow(x, 1)']
        ]
        for pair in lst:
            self.assertEqual(get_simplified_expr_from_string(pair[0]), pair[1])



def test(cls):
    suite = unittest.TestLoader().loadTestsFromTestCase(cls)
    unittest.TextTestRunner(verbosity=2).run(suite)


def main():
    test(TestSimplification)

main()
    

lst = ['1/sin(x)', '1.00*pow(1.00*sin(1.00*x), -1.00)', 'pow(sin(x), -1)', '1/pow(sin(x), 1)', 'x']
lst = ['1/x', '1/pow(x, 1)', 'pow(x, -1)']
#lst = ['x']

for i in lst:
    tokens = Tokens(i)
    expr = get_expr(tokens)
#    print(expr)
    expr.simplify()
#    dist_term(expr.term)
    #expr.gather_coefficient()
    print('\n', i, '\nbecomes', expr)
    #dist_term(expr.term)
    #print expr

