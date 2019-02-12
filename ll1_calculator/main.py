from my_tokenizer import tokenizer
from ll1_parser import get_expr
import unittest

def expr_from_string(s):
    lst = tokenizer(s)
    return get_expr(lst)

def expr_str(s):
    expr = expr_from_string(s)
    return str(expr)

def expr_eval(s):
    expr = expr_from_string(s)
    return expr.eval()
    

class TestGraph(unittest.TestCase):

    def test_simple(self):
        self.assertEqual(expr_str('2+3'), '2+3')

    def test_multi_ops(self):
        self.assertEqual(expr_str('2 + 3 * 5'), '2+3*5')

    def test_parens(self):
        self.assertEqual(expr_str('3*(2 + 3 / 2)'), '3*(2+3/2)')

class TestEvaluation(unittest.TestCase):

    def test_plus(self):
        self.assertEqual(expr_eval('2 + 3'), 5.0)

    def test_minus(self):
        self.assertEqual(expr_eval('4 - 9'), -5.0)

    def test_mul(self):
        self.assertEqual(expr_eval('4*9'), 36.0)

    def test_float_div(self):
        self.assertEqual(expr_eval('2/5.'), 0.4)

    def test_int_div(self):
        self.assertEqual(expr_eval('3/2'), 1)

    def test_parens(self):
        self.assertEqual(expr_eval('3*(3/2.+2)'), 10.5)

def test(cls):
    suite = unittest.TestLoader().loadTestsFromTestCase(cls)
    unittest.TextTestRunner(verbosity=2).run(suite)

def main():
    test(TestGraph)
    test(TestEvaluation)
    s = ''
    while s != 'q':
        s = input("Enter the formula(to exit, type 'q'):\n")
        tokens = tokenizer(s)
        E = get_expr(tokens)
        if len(tokens)>0:
            raise SyntaxError("Unexpected token : longer than correct expression")
        print('=', E.eval())

if __name__ == "__main__":
    main()
