from my_tokenizer import Tokens
from tree_generator import *
from simplifier import *
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
    

lst = ['sin(x)', '1/sin(x)', 'pow(sin(pow(x, 1)), -1)', 'pow(sin(x), -1)', '1/pow(sin(x), 1)']
#lst = ['1/x', '1/pow(x, 1)', 'pow(x, -1)']
#lst = ['2*3-4*5']

for s in lst:
    expr = get_simple_expr(s)
#    print(expr)
#    dist_term(expr.term)
    #expr.gather_coefficient()
    print(s, '\nbecomes', expr, '\n')
    #dist_term(expr.term)
    #print expr


ex1 = get_meta_expr('pow(x, 2)*pow(x, 3)*x')
ex2 = get_meta_expr('pow(x, 3)')
ex3 = ex1+ex2

print('%s plus\n%s is\n%s\n'%(ex1, ex2, ex3))
