import unittest
from my_tokenizer import Tokens
from tree_generator import *
from evaluator import eval_meta, is_continuous, is_differentiable
from differentiator import diff_meta


class TestSimplification(unittest.TestCase):

    def test_numbers(self):
        lst = (('2*3', '6'),
               ('2*3*-4', '-24'),
               ('2*-3*2', '-12'),
               ('3/2*4', '6')
              )
        for pair in lst:
            self.assertEqual(str(get_simple_expr(pair[0])), get_simple_expr(pair[1]))

    def test_variables(self):
        lst = (('x', 'pow(x, 1)'),
               ('2*x', '2*pow(x, 1)'),
               ('x*3', '3*pow(x, 1)'),
               ('1/x', 'pow(x, -1)'),
               ('x*y/x', 'pow(x, 1)*pow(x, -1)*pow(y, 1)'),
               ('x*x', 'pow(x, 2)'),
               ('pow(x, 3)', 'pow(x, 3)'),
              )
        for pair in lst:
            self.assertEqual(str(get_simple_expr(pair[0])), get_simple_expr(pair[1]))

    def test_constants(self):
        lst = (('e', 'pow(e, 1)'),
               ('2*pi', '2*pow(pi, 1)'),
               ('e*3', '3*pow(e, 1)'),
               ('1/pi', 'pow(pi, -1)'),
               ('pi*e/pi', 'pow(e, 1)'),
               ('1/(pi)', 'pow(pi, -1)'),
        )
        for pair in lst:
            self.assertEqual(str(get_simple_expr(pair[0])), get_simple_expr(pair[1]))

    def test_pow(self):
        lst = (('1/x', 'pow(x, -1)'),
               ('-1/-x', '1/x'),
               ('1/(2*x)', '0.5/x'),
               ('2/(2*x)', '1/x'),
               ('1.5/(1.5*x)', '1/x'),
               ('x/(x*y)', '1/x/y*x'),
               ('pow(pow(x, 1), 1)', 'pow(x, 1)'),
               ('pow(pow(x, 2), 3)', 'pow(x, 6)'),
               ('1/pow(x, 1)', 'pow(x, -1)'),
               ('pow(2*x, 2)', '4*pow(x, 2)'),
               ('pow(x*y, 1)', 'pow(y, 1)*pow(x, 1)'),
               ('pow(2*x*y, 2)', '4*pow(y, 2)*pow(x, 2)'),
               ('1/pow(x*(y+2), 2)', 'pow(x, -2)*pow(pow(y, 1)+2, -2)'),
               ('x*(x+y)', 'x*pow(x+y, 1)')
        )
        for pair in lst:
            self.assertEqual(str(get_simple_expr(pair[0])), get_simple_expr(pair[1]))

    def test_distribution(self):
        lst = (('pow(2*(x+y), 1.5)', '2.828427*pow(pow(y, 1)+pow(x, 1), 1.5)'),
               ('pow(x+y, 2)', 'pow(y, 2)+2*pow(y, 1)*pow(x, 1)+pow(x, 2)'),
               ('pow(x+1, 3)', 'pow(x, 3)+3*pow(x, 2)+3*pow(x, 1)+1'),
               ('(x-y)*(pow(x, 2) + x*y + pow(y, 2))', 'pow(x, 3) - pow(y, 3)')
        )
        for pair in lst:
            self.assertEqual(str(get_simple_expr(pair[0])), get_simple_expr(pair[1]))

    def test_paren(self):
        lst = (('(2)', '2'),
               ('(x)', 'x'),
               ('1/(x)', '1/x'),
               ('-1/(-x)', '1/x'),
               ('1/(x+y)', 'pow(x+y, -1)'),
               ('pow(2*(x), 2)', 'pow(2*x, 2)'),
               ('1/(pow(x, 1))', 'pow(x, -1)'),
               ('1/(pow(x, -1))', 'pow(x, 1)'),
               ('pow((2*x+4*y), 1.5)', 'pow(4, 1.5)*pow(0.5*x+y, 1.5)'),
               ('(((((((((x)))))+y))))', 'x+y')
        )
        for pair in lst:
            self.assertEqual(str(get_simple_expr(pair[0])), get_simple_expr(pair[1]))

    def test_trigonometric(self):
        lst = (('sin(x)', 'pow(sin(pow(x, 1)), 1)'),
               ('1/sin(x)', 'pow(sin(pow(x, 1)), -1)'),
               ('pow(sin(x), -1)', 'pow(sin(pow(x, 1)), -1)'),
               ('1/pow(sin(x), 1)', 'pow(sin(pow(x, 1)), -1)'),
               ('cos(x)*tan(x)', 'sin(x)*cos(x)/cos(x)'),
               ('sin(x)/tan(x)', 'cos(x)/sin(x)*sin(x)'),
               ('-sin(x)', '-pow(sin(x), 1)')
        )
        for pair in lst:
            self.assertEqual(str(get_simple_expr(pair[0])), get_simple_expr(pair[1]))

    def test_log(self):
        lst = (('log(x)', 'pow(log(pow(x, 1)), 1)'),
               ('log(x*y)', 'log(x)+log(y)'),
               ('log(x*(y+2))', 'log(x)+log(y+2)'),
               ('log(e)', '1'),
               ('log(pi)', 'pow(log(pi), 1)'),
               ('log(pow(e, 1))', '1'),
               ('log(pow(e, 3))', '3'),
               ('pow(log(pow(e, 2)), 2)', '4'),
        )
        for pair in lst:
            self.assertEqual(str(get_simple_expr(pair[0])), get_simple_expr(pair[1]))

class TestEvaluation(unittest.TestCase):

    def test_eval_meta(self):
        lst = (('2', 0, 2),
               ('x+2', 2, 4),
               ('pow(x, 3)', 3, 27),
               ('log(x)', 'e', 1),
               ('cos(x)', 'pi/2', 0),
        )
        for pair in lst:
            self.assertEqual(eval_meta(get_meta_expr(pair[0]), pair[1]), pair[2])

    def test_continuity_check(self):
        lst = (('1/sin(x)', '-5*pi', False),
               ('1/x', 0, False),
               ('pow(pow(x, 2), 1/2)', '0', True),
               ('pow(x, 1/2)*pow(x, 1/2)', '0', True),
               ('x + x*pow(pow(x, 2), -0.5)', '0', False),
        )
        for pair in lst:
            self.assertEqual(is_continuous(get_meta_expr(pair[0]), pair[1]), pair[2])

    def test_differentiability_check(self):
        lst = (('1/sin(x)', '-5*pi', False),
               ('1/x', 0, False),
               ('pow(pow(x, 2), 1/2)', 0, False),
               ('pow(x, 1/2)*pow(x, 1/2)', 0, False),
               ('x + x*pow(pow(x, 2), -0.5)', 0, False),
        )
        for pair in lst:
            self.assertEqual(is_differentiable(get_meta_expr(pair[0]), pair[1]), pair[2])


class TestDifferentiation(unittest.TestCase):

    def test_numbers(self):
        lst = (('2', '0'),
               ('3*4', '0'),
               ('0*3 +4', '0'),
        )
        for pair in lst:
            self.assertEqual(diff_meta(get_meta_expr(pair[0])), get_meta_expr(pair[1]))

    def test_func(self):
        lst = (('sin(x)', 'cos(x)'),
               ('cos(x)', '-sin(x)'),
               ('log(x)', '1/x'),
               ('1/sin(x)', '-cos(x)/sin(x)/sin(x)'),
               ('pow(e, x)', 'pow(e, x)'),
               ('pow(2, x)', '0.693147*pow(2, x)'),
               ('log(sin(x))', 'pow(tan(x), -1)'),
               ('log(y)', '0'),
        )
        for pair in lst:
            self.assertEqual(diff_meta(get_meta_expr(pair[0])), get_meta_expr(pair[1]))


def test(cls):
    suite = unittest.TestLoader().loadTestsFromTestCase(cls)
    unittest.TextTestRunner(verbosity=2).run(suite)

def main():
    tests = [TestSimplification, TestEvaluation, TestDifferentiation]
    for t in tests:
        test(t)

if (__name__ == "__main__"):
    main()
