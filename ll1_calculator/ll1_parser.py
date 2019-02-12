import re

def is_add_op(op):
    add_ops = ['+', '-']
    return op in add_ops

def is_mul_op(op):
    mul_ops = ['*', '/']
    return op in mul_ops

def is_int(num):
    lst = re.split('(0|-?[1-9][0-9]*)', num)
    return lst[0] == '' and lst[2] == '' and lst[1] == num and len(lst) == 3

def is_num(num):
    lst = re.split('(0|-?0\.[0-9]*|-?[1-9][0-9]*\.?[0-9]*)', num)
    return lst[0] == '' and lst[2] == '' and lst[1] == num and len(lst) == 3

def get_expr(tokens):
    monomial = get_mono(tokens)
    poly_tail = get_ptail(tokens)
    return Expr(monomial, poly_tail)

def get_ptail(tokens):
    if len(tokens) > 0 and is_add_op(tokens[0]):
        op = tokens.pop(0)
        expr = get_expr(tokens)
        return PTail(op, expr)
    else:
        return PTail('', Empty())

def get_mono(tokens):
    factor = get_factor(tokens)
    mono_tail = get_mtail(tokens)
    return Mono(factor, mono_tail)

def get_mtail(tokens):
    if len(tokens) > 0 and is_mul_op(tokens[0]):
        op = tokens.pop(0)
        monomial = get_mono(tokens)
        return MTail(op, monomial)
    else:
        return MTail('', Empty())

def get_factor(tokens):
    if tokens[0] == '(':
        factor = get_paren(tokens)
    else:
        factor = get_num(tokens)
    return factor

def get_paren(tokens):
    tokens.pop(0)
    expr = get_expr(tokens)
    this = tokens.pop(0)
    if this == ')':
        return Paren(expr)
    else:
        raise SyntaxError("Unexpected ')'")

def get_num(tokens):
    num = tokens.pop(0)
    if num == '-' and is_num(tokens[0]):
        return Num(num + tokens.pop(0))
    elif is_num(num):
        return Num(num)
    else:
        raise SyntaxError("Unexpected token(should be a number)")

def calculate(first, op, second):
    if first.ntype == 1:
        a = int(first.eval())
    else:
        a = float(first.eval())
    if op == '':
        return a
    if second.ntype == 1:
        b = int(second.eval())
    else:
        b = float(second.eval())

    if type(a) != type(b):
        raise TypeError("type of two operands are different!")
    if op == '+':
        return a + b
    elif op == '-':
        return a - b
    elif op == '*':
        return a * b
    elif op == '/':
        return a / b
    else:
        raise ValueError("Unexpected operator")

class Expr:
    def __init__(self, mono, ptail):
        self.mono = mono
        self.ptail = ptail
        self.ntype = mono.ntype * ptail.expr.ntype

        if not self.ntype:
            mono.ntype = 0
            ptail.expr.ntype = 0

    def eval(self):
        return calculate(self.mono, self.ptail.op, self.ptail.expr)

    def __str__(self):
        return str(self.mono) + str(self.ptail)

class PTail:
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

    def __str__(self):
        return str(self.op) + str(self.expr)

class Mono:
    def __init__(self, factor, mtail):
        self.factor = factor
        self.mtail = mtail
        self.ntype = factor.ntype * mtail.mono.ntype
        if not self.ntype:
            factor.ntype = 0
            mtail.mono.ntype = 0

    def eval(self):
        return calculate(self.factor, self.mtail.op, self.mtail.mono)

    def __str__(self):
        return str(self.factor) + str(self.mtail)

class MTail:
    def __init__(self, op, mono):
        self.op = op
        self.mono = mono

    def __str__(self):
        return str(self.op) + str(self.mono)

class Paren:
    def __init__(self, expr):
        self.expr = expr
        self.ntype = self.expr.ntype

    def eval(self):
        return self.expr.eval()

    def __str__(self):
        return '(' + str(self.expr) + ')'

class Num:
    def __init__(self, num):
        self.num = num
        if is_int(num):
            self.ntype = 1
        else:
            self.ntype = 0

    def eval(self):
        if is_int(self.num):
            return int(self.num)
        else:
            return float(self.num)

    def __str__(self):
        return str(self.num)
    
class Empty:
    def __init__(self):
        self.ntype = 1

    def eval(self):
        return None

    def __str__(self):
        return ''
