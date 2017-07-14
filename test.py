import unittest
from my_tokenizer import Tokens
from tree_generator import *


class TestSimplification(unittest.TestCase):

    def test_numbers(self):
        lst = (('2*3', '6.000000'),
               ('2*3*-4', '-24.000000'),
               ('2*-3*2', '-12.000000'),
               ('3/2*4', '6.000000')
              )
        for pair in lst:
            self.assertEqual(str(get_simple_expr(pair[0])), get_simple_expr(pair[1]))

    def test_variables(self):
        lst = (('x', 'pow(x, 1)'),
               ('2*x', '2.000000*pow(x, 1)'),
               ('x*3', '3.000000*pow(x, 1)'),
               ('1/x', 'pow(x, -1)'),
               ('x*y/x', 'pow(y, 1)'),
               ('x*x', 'pow(x, 2.000000)'),
               ('pow(x, 3)', 'pow(x, 3.000000)'),
              )
        for pair in lst:
            self.assertEqual(str(get_simple_expr(pair[0])), get_simple_expr(pair[1]))

    def test_constants(self):
        lst = (('e', 'pow(e, 1)'),
               ('2*pi', '2.000000*pow(pi, 1)'),
               ('e*3', '3.000000*pow(e, 1)'),
               ('1/pi', 'pow(pi, -1)'),
               ('pi*e/pi', 'pow(e, 1)'),
               ('1/(pi)', 'pow(pi, -1)'),
        )
        for pair in lst:
            self.assertEqual(str(get_simple_expr(pair[0])), get_simple_expr(pair[1]))

    def test_pow(self):
        lst = (('1/x', 'pow(x, -1)'),
               ('pow(pow(x, 1), 1)', 'pow(x, 1)'),
               ('pow(pow(x, 2), 3)', 'pow(x, 6.000000)'),
               ('1/pow(x, 1)', 'pow(x, -1)'),
               ('pow(2*x, 2)', '4.000000*pow(x, 2.000000)'),
               ('pow(x*y, 1)', 'pow(y, 1)*pow(x, 1)'),
               ('pow(2*x*y, 2)', '4.000000*pow(y, 2.000000)*pow(x, 2.000000)'),
               ('1/pow(x*(y+2), 2)', 'pow(x, -2.000000)*pow(pow(y, 1)+2.000000, -2.000000)'),
        )
        for pair in lst:
            self.assertEqual(str(get_simple_expr(pair[0])), get_simple_expr(pair[1]))

    def test_distribution(self):
        lst = (('pow(2*(x+y), 1.5)', '2.828427*pow(pow(y, 1)+pow(x, 1), 1.500000)'),
               ('pow(x+y, 2)', 'pow(y, 2.000000)+2.000000*pow(y, 1)*pow(x, 1)+pow(x, 2.000000)'),
               ('pow(x+1, 3)', 'pow(x, 3.000000)+3.000000*pow(x, 2.000000)+3.000000*pow(x, 1)+1'),
               ('pow(8*x+4*y, 0.5)*pow(2*x+y, 1.5)', '2.000000*pow(y, 2.000000)+8.000000*pow(y, 1)*pow(x, 1)+8.000000*pow(x, 2.000000)'),
               ('pow(0.5*x+y, 0.2)*pow(2*x+4*y, 1.5)*pow(0.5*x+y, 1.3)', '8.000000*pow(y, 3.000000)+12.000000*pow(y, 2.000000)*pow(x, 1)+6.000000*pow(y, 1)*pow(x, 2.000000)+pow(x, 3.000000)'),
               ('pow(2*x+4*y, 1.5)', '8.000000*pow(pow(y, 1)+0.500000*pow(x, 1), 1.500000)'),
        )
        for pair in lst:
            self.assertEqual(str(get_simple_expr(pair[0])), get_simple_expr(pair[1]))

    def test_paren(self):
        lst = (('(2)', '2'),
               ('(x)', 'x'),
               ('1/(x)', '1/x'),
               ('1/(x+y)', 'pow(x+y, -1)'),
               ('pow(2*(x), 2)', 'pow(2*x, 2)'),
               ('1/(pow(x, 1))', 'pow(x, -1)'),
               ('1/(pow(x, -1))', 'pow(x, 1)'),
               ('pow((2*x+4*y), 1.5)', 'pow(4, 1.5)*pow(0.5*x+y, 1.5)')
        )
        for pair in lst:
            self.assertEqual(str(get_simple_expr(pair[0])), get_simple_expr(pair[1]))

    def test_trigonometric(self):
        lst = (('sin(x)', 'pow(sin(pow(x, 1)), 1)'),
               ('1/sin(x)', 'pow(sin(pow(x, 1)), -1)'),
               ('pow(sin(x), -1)', 'pow(sin(pow(x, 1)), -1)'),
               ('1/pow(sin(x), 1)', 'pow(sin(pow(x, 1)), -1)'),
               ('cos(x)*tan(x)', 'sin(x)'),
               ('sin(x)/tan(x)', 'cos(x)'),
        )
        for pair in lst:
            self.assertEqual(str(get_simple_expr(pair[0])), get_simple_expr(pair[1]))

    def test_(self):
        lst = (
        )
        for pair in lst:
            self.assertEqual(str(get_simple_expr(pair[0])), get_simple_expr(pair[1]))

    def test_(self):
        lst = (
        )
        for pair in lst:
            self.assertEqual(str(get_simple_expr(pair[0])), get_simple_expr(pair[1]))

    def test_(self):
        lst = (
        )
        for pair in lst:
            self.assertEqual(str(get_simple_expr(pair[0])), get_simple_expr(pair[1]))

    def test_(self):
        lst = (
        )
        for pair in lst:
            self.assertEqual(str(get_simple_expr(pair[0])), get_simple_expr(pair[1]))


def test(cls):
    suite = unittest.TestLoader().loadTestsFromTestCase(cls)
    unittest.TextTestRunner(verbosity=2).run(suite)

def main():
    tests = [TestSimplification]
    for t in tests:
        test(t)

main()
