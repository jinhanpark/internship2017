import string
import unittest

opers = {'+' : 1, '-' : 1,
         '*' : 2, '/' : 2,
         '(' : 0, ')' : 0}

class TestPostfixCalc(unittest.TestCase):

    def test_plus(self):
        self.assertEqual(eval_raw('2+3'), 5.0)

    def test_minus(self):
        self.assertEqual(eval_raw('1-4'), -3.0)

    def test_mul(self):
        self.assertEqual(eval_raw('7*8'), 56.0)

    def test_div(self):
        self.assertEqual(eval_raw('3/2'), 1.5)

    def test_paren(self):
        self.assertEqual(eval_raw('(2 + 3) * 6'), 30.0)

class TestRpnGenerating(unittest.TestCase):

    def test_simple(self):
        self.assertEqual(rpnstr('2 + 3'), '2 3 +')

    def test_multi_ops(self):
        self.assertEqual(rpnstr('2 + 3 * 5'), '2 3 5 * +')

    def test_rpn_with_parens(self):
        self.assertEqual(rpnstr('5*(2+3)'), '2 3 + 5 *')

def test(cls):
    suite = unittest.TestLoader().loadTestsFromTestCase(cls)
    unittest.TextTestRunner(verbosity=2).run(suite)

def str_to_lst(s):
    global opers
    for i in opers:
        s = string.replace(s, i, ' '+i+' ')
    return s.split()

def raw_to_rpn(s): # rpn stands for "reverse Polish notation"
    global opers
    lst = str_to_lst(s)
    rpn_stack = []
    op_stack = []
    for i in lst:
        if i == ')':
            while(op_stack[-1] != '('):
                rpn_stack.append(op_stack.pop())
            op_stack.pop()
        elif i in opers:
            while(len(op_stack) != 0 and
                  opers[op_stack[-1]] >= opers[i] and
                  i != '('):
                rpn_stack.append(op_stack.pop())
            op_stack.append(i)
        else:
            rpn_stack.append(i)
    op_stack.reverse()
    rpn_stack.extend(op_stack)
    return rpn_stack

def rpn_to_str(rpn):
    return string.join(rpn)

def rpnstr(s):
    rpn = raw_to_rpn(s)
    return rpn_to_str(rpn)

def calc(a, b, o):
    if o == '+':
        return a + b
    elif o == '-':
        return a - b
    elif o == '*':
        return a * b
    elif o == '/':
        return a / b

def eval_rpn(lst):
    global opers
    temp_stack = []
    for i in lst:
        if i in opers:
            b = float(temp_stack.pop())
            a = float(temp_stack.pop())
            temp_stack.append(calc(a, b, i))
        else:
            temp_stack.append(i)
    return temp_stack[0]

def eval_raw(s):
    global opers
    rpn = raw_to_rpn(s)
    return eval_rpn(rpn)

def main():
    test(TestPostfixCalc)
    test(TestRpnGenerating)
    s = ''
    while(s != 'q'):
        s = raw_input("Enter the formula(to exit, 'q'):\n")
        print '=', eval_raw(s)

if __name__ == "__main__":
    main()
