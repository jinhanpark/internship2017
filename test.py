from my_tokenizer import Tokens
from tree_generator import *

import unittest
#import sys
#sys.setrecursionlimit(10000)

class TestSimplification(unittest.TestCase):

    def test_get_coeff(self):

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
    

lst = ['sin(x)', '1/sin(x)', 'pow(sin(pow(x, 1)), -1)', 'pow(sin(x), -1)', '1/pow(sin(x), 1)', 'cos(x)*tan(x)', 'sin(x)/tan(x)']
#lst = ['1/x', '1/pow(x, 1)', 'pow(x, -1)']
lst = ['pow(x*y, 1)', 'pow(x*y, 2)', 'pow(2*x*5*y*3, 2)']
lst = ['pow(2*(x+y), 1.5)', 'pow(x+y, 2)', 'pow(x+1, 3)', 'sin(x)', 'cos(x)*tan(x)', 'log(x)']



for s in lst:
    expr = get_simple_expr(s)
#    print(expr)
#    dist_term(expr.term)
    #expr.gather_coefficient()
    print(s, '\nbecomes', expr, '\n')
    #dist_term(expr.term)
    #print expr


# ex1 = get_meta_expr('pow(2, 2)')
# ex2 = get_meta_expr('pow(2, 3)')
# ex3 = ex1+ex2

# print('%s plus\n%s is\n%s\n'%(ex1, ex2, ex3))

# ex1 = get_expr_from_string('pow(2*x*y, 3)')
# base = ex1.term.factor.base
