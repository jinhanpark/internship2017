import math

class Empty:
    def __init__(self):
        pass

    def simplify(self):
        pass

    def __str__(self):
        return ''

class Expr:
    def __init__(self, term, extail=Empty()):
        self.term = term
        self.extail = extail

    def simplify(self):
        self.term.simplify()
        self.extail.simplify()
        self.term.powerize()
        self.term.get_coeff()
        self.term.remove_nums()

    def eval(self):
        pass

    def __str__(self):
        coeff = self.term.coeff
        coeff_str = '%.2f*'%coeff
        if coeff == 1.0:
            coeff_str = ''
        elif coeff == -1.0:
            coeff_str = '-'
        elif isinstance(self.term.factor, Num):
            coeff_str = '%.2f'%coeff
            if isinstance(self.term.termtail, Empty):
                return '%s%s'%(coeff_str, str(self.extail))
            else:
                return '%s%s%s'%(coeff_str, str(self.term.termtail), str(self.extail))

        return '%s%s%s'%(coeff_str, str(self.term), str(self.extail))

    def __neg__(self):
        self.term = -self.term
        if not isinstance(self.extail, Empty):
            self.extail.expr = -self.extail.expr
        return self


    def __add__(self, another):
        return '%s+%s'%(str(self), str(another))

class ExTail:
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

    def simplify(self):
        if self.op == '-':
            self.op = '+'
            self.expr.term.coeff *= -1
        self.expr.simplify()


    def __str__(self):
        return str(self.op) + str(self.expr)

class Term:
    def __init__(self, factor, termtail=Empty()):        
        self.factor = factor
        self.termtail = termtail
        self.coeff = 1

    def add_term_tail(self, tail):
        temp = self
        while temp.termtail.type != 'empty':
            temp = temp.termtail.term
        temp.termtail = tail

    def powerize(self, ind=1):
        self.factor = self.factor.powerized(ind)
        if not isinstance(self.termtail, Empty):
            if self.termtail.op == '/':
                self.termtail.op  = '*'
                ind = -1
            self.termtail.term.powerize(ind)

    def get_coeff(self):
        self.coeff *= self.factor.coeff
        self.factor.coeff = 1
        if not isinstance(self.termtail, Empty):
            self.termtail.term.get_coeff()
            self.coeff *= self.termtail.term.coeff
            self.termtail.term.coeff = 1

    def remove_nums(self):
        self.remove_right_nums()
        self.remove_left_num()

    def remove_right_nums(self):
        if not isinstance(self.termtail, Empty):
            if isinstance(self.termtail.term.factor, Num): # remove tail nums
                self.termtail.term.remove_right_nums()
                self.termtail = self.termtail.term.termtail
            else:
                self.termtail.term.remove_right_nums()

    def remove_left_num(self):
        if isinstance(self.factor, Num) and\
           not isinstance(self.termtail, Empty): # remove last first num if it has nonempty tail
            self.factor = self.termtail.term.factor
            self.termtail = self.termtail.term.termtail


    def simplify(self):
        self.factor.simplify()
        self.termtail.simplify()

    def eval(self):
        pass

    def __str__(self):
        return '%s%s'%(str(self.factor), str(self.termtail))

    def __neg__(self):
        self.coeff *= -1
        return self

class TermTail:
    def __init__(self, op, term):
        self.op = op
        self.term = term

    def simplify(self):
        self.term.simplify()

    def __str__(self):
        return str(self.op) + str(self.term)

class Factor:
    def __init__(self, coeff):
        self.coeff = coeff

    def simplify(self):
        pass

    def powerized(self, ind=1):
        base_expr = factor2expr(self)
        ind_expr = number2expr(ind)
        return Pow(base_expr, ind_expr)

class Pow(Factor):
    def __init__(self, base, ind, coeff=1):
        Factor.__init__(self, coeff)
        self.base = base
        self.ind = ind

    def simplify(self):
        self.base.simplify()
        self.ind.simplify()

    def powerized(self, ind=1):
        if ind == -1:
            self.ind = -self.ind
        return self

    def eval(self):
        pass

    def __str__(self):
        return 'pow(%s, %s)'%(str(self.base), str(self.ind))

class Var(Factor):
    def __init__(self, var, coeff = 1):
        Factor.__init__(self, coeff)
        self.var = var

    def eval(self):
        pass

    def __str__(self):
        return str(self.var)

class Const(Factor):
    def __init__(self, const, coeff = 1):
        Factor.__init__(self, coeff)
        self.const = const

    def eval(self):
        pass

    def __str__(self):
        return str(self.const)

class Num():
    def __init__(self, num, coeff = 1):
        self.coeff = float(num) * coeff
        self.num = 1

    def simplify(self):
        pass

    def powerized(self, ind=1):
        self.coeff = math.pow(self.coeff, ind)
        return self

    def eval(self):
        pass

    def __str__(self):
        # if self.num == 1: #delete *1's
        #     return '\b'
        return str(self.coeff)

class SingleFunction(Factor):
    def __init__(self, expr, coeff=1):
        Factor.__init__(self, coeff)
        self.expr = expr

    def simplify(self):
        self.expr.simplify()

    def __str__(self):
        return '%s(%s)'%(self.func_name, str(self.expr))

class Paren(SingleFunction): #regard Paren as identity function
    def __init__(self, expr, coeff=1):
        SingleFunction.__init__(self, expr, coeff)
        self.func_name = ''

    def eval(self):
        pass

class Sin(SingleFunction):
    def __init__(self, expr, coeff=1):
        SingleFunction.__init__(self, expr, coeff)
        self.func_name = 'sin'

    def eval(self):
        pass

class Cos(SingleFunction):
    def __init__(self, expr, coeff=1):
        SingleFunction.__init__(self, expr, coeff)
        self.func_name = 'cos'

    def eval(self):
        pass

class Tan(SingleFunction):
    def __init__(self, expr, coeff=1):
        SingleFunction.__init__(self, expr, coeff)
        self.func_name = 'tan'

    def powerized(self, ind):        
        sin_ind = number2expr(ind)
        cos_ind = number2expr(-ind)
        self.expr.powerize()
        sin = factor2expr(Sin(self.expr))
        cos = factor2expr(Cos(self.expr))
        expr = multiply_factors2expr(Pow(sin, sin_ind),
                                     Pow(cos, cos_ind))
        return Paren(expr, self.coeff)

    def eval(self):
        pass

class ArcSin(SingleFunction):
    def __init__(self, expr, coeff=1):
        SingleFunction.__init__(self, expr, coeff)
        self.func_name = 'arcsin'

    def eval(self):
        pass

class ArcCos(SingleFunction):
    def __init__(self, expr, coeff=1):
        SingleFunction.__init__(self, expr, coeff)
        self.func_name = 'arccos'

    def eval(self):
        pass

class ArcTan(SingleFunction):
    def __init__(self, expr, coeff=1):
        SingleFunction.__init__(self, expr, coeff)
        self.func_name = 'arctan'

    def eval(self):
        pass

class Log(SingleFunction):
    def __init__(self, expr, coeff=1):
        SingleFunction.__init__(self, expr, coeff)
        self.func_name = 'log'

    def eval(self):
        pass

def factor2expr(given):
    temp = Expr(Term(given))
    return temp

def number2expr(given):
    temp = Expr(Term(Num(given)))
    temp.simplify()
    return temp

def expr2paren(given):
    temp = Expr(Term(Paren(given)))
    return temp

def multiply_factors2expr(given1, given2):
    temp = Expr(Term(given1, TermTail('*', Term(given2))))
    return temp
