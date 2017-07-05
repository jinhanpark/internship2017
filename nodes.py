import math
import copy

class Empty:
    def __init__(self):
        self.type = 'empty'

    def gather_coefficient(self):
        pass

    def powerize(self):
        pass

    def __str__(self):
        return ''

class Expr:
    def __init__(self, term, extail=Empty()):
        self.type = 'expr'
        self.term = term
        self.extail = extail
        self.term.coeff = 'not gathered'
        self.gather_coefficient()

    def gather_coefficient(self):
        self.term.gather_coefficient()
        self.extail.gather_coefficient()
        
    def powerize(self):
        self.term.powerize()
        self.extail.powerize()

    def simplify(self):
        self.powerize()
        self.gather_coefficient()

    def eval(self):
        pass

    def __str__(self):
        coeff = self.term.coeff
        if type(coeff) == str:
            coeff_str = coeff
        elif coeff != 1.0 or True:
            coeff_str = '%.2f*'%coeff
        else:
            coeff_str = ''
        return '%s%s%s'%(coeff_str, str(self.term), str(self.extail))

    def __neg__(self):
        if self.extail.type == 'empty':
            self.term.coeff *= -1
            return self
        else:
            raise SyntaxError("negation on expression which has tail")

class ExTail:
    def __init__(self, op, expr):
        self.type = 'extail'
        self.op = op
        self.expr = expr

    def gather_coefficient(self):
        self.expr.gather_coefficient()

    def powerize(self):
        self.expr.powerize()

    def __str__(self):
        return str(self.op) + str(self.expr)

class Term:
    def __init__(self, factor, termtail=Empty()):        
        self.type = 'term'
        self.factor = factor
        self.termtail = termtail
        self.coeff = None

    def add_tail(self, tail):
        temp = self
        while temp.termtail.type != 'empty':
            temp = temp.termtail.term
        temp.termtail = tail

    def gather_coefficient(self):
        self.factor.gather_coefficient()
        self.termtail.gather_coefficient()

        self.get_coeff_and_remove_num()

    def powerize(self, ind=1):
        ind = num2expr(ind)
        self.factor = self.factor.powerized(ind)
        if self.termtail.type == 'empty':
            pass
        elif self.termtail.op == '/':
            self.termtail.op = '*'
            self.termtail.term.powerize(-1)
        else:
            self.termtail.term.powerize()

    def get_coeff_and_remove_num(self):
        coeff = self.coeff
        if coeff != 'not gathered':
            return None
        if self.factor.type != 'num':
            self.coeff = 'ignore'
            self.termtail = TermTail('*', copy.deepcopy(self))
            self.factor = Num(1)
        coeff = self.factor.coeff
        temp = self
        while temp.termtail.type != 'empty':
            next_factor = temp.termtail.term.factor
            next_termtail = temp.termtail.term.termtail
            if temp.termtail.op == '*':
                coeff *= next_factor.coeff
            elif temp.termtail.op == '/':
                coeff /= next_factor.coeff
            next_factor.coeff = 1
            if next_factor.type == 'num':
                temp.termtail = next_termtail
            else:
                temp = temp.termtail.term
        self.coeff = coeff

    def eval(self):
        pass

    def __str__(self):
        return '%s%s'%(str(self.factor), str(self.termtail))

class TermTail:
    def __init__(self, op, term):
        self.type = 'termtail'
        self.op = op
        self.term = term

    def gather_coefficient(self):
        self.term.gather_coefficient()

    def __str__(self):
        return str(self.op) + str(self.term)

class Factor:
    def __init__(self, coeff):
        self.type = 'factor'
        self.coeff = coeff

    def gather_coefficient(self):
        pass

    def powerized(self, ind):
        new = factor2expr(self)
        return Pow(new, ind, self.coeff)
        
class SingleFunction(Factor):
    def __init__(self, expr, coeff=1):
        Factor.__init__(self, coeff)
        self.type = 'func'
        self.expr = expr
        self.func_name = ''

    def gather_coefficient(self):
        self.expr.gather_coefficient()

    def powerized(self, ind):
        self.expr.powerize()
        new = factor2expr(self)
        return Pow(new, ind, self.coeff)

    def __str__(self):
        return '%s(%s)'%(self.func_name, str(self.expr))

class Paren(SingleFunction): #regard Paren as identity function
    def __init__(self, expr, coeff=1):
        SingleFunction.__init__(self, expr, coeff)
        self.type = 'paren'

    def powerized(self, ind):
        self.expr.powerize()
        if ind.term.coeff == -1:
            return Pow(self.expr, ind)
        else:
            return self

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
        sin_ind = ind
        cos_ind = -copy.deepcopy(ind)
        self.expr.powerize()
        sin = factor2expr(Sin(self.expr))
        cos = factor2expr(Cos(self.expr))
        new = multiply_factors2expr(Pow(sin, sin_ind),
                                 Pow(cos, cos_ind))
        return Paren(new, self.coeff)

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

class Pow(Factor):
    def __init__(self, base, ind, coeff=1):
        Factor.__init__(self, coeff)
        self.type = 'pow'
        self.base = base
        self.ind = ind
        self.func_name = 'pow'

    def gather_coefficient(self):
        self.base.gather_coefficient()
        self.ind.gather_coefficient()

    def powerized(self, ind):
        self.ind.powerize()
        if self.ind.extail.type != 'empty':
            self.ind = expr2paren(self.ind)
        self.base.powerize()
        self.ind.term.coeff *= ind.term.coeff
        return self

    def eval(self):
        pass

    def __str__(self):
        return 'pow(%s, %s)'%(str(self.base), str(self.ind))

class Var(Factor):
    def __init__(self, var, coeff = 1):
        Factor.__init__(self, coeff)
        self.type = 'var'
        self.var = var

    def eval(self):
        pass

    def __str__(self):
        return str(self.var)

class Const(Factor):
    def __init__(self, const, coeff = 1):
        Factor.__init__(self, coeff)
        self.type = 'const'
        self.const = const

    def eval(self):
        pass

    def __str__(self):
        return str(self.const)

class Num():
    def __init__(self, num, coeff = 1):
        self.type = 'num'
        self.num = float(num)
        self.coeff = coeff

    def gather_coefficient(self):
        self.coeff = self.num * self.coeff
        self.num = 1

    def powerized(self, ind):
        self.coeff = math.pow(self.coeff, ind.term.coeff)
        return self

    def eval(self):
        pass

    def __str__(self):
        if self.num == 1: #delete *1's
            return '\b'
        return str(self.num)


def factor2expr(given):
    temp = Expr(Term(given))
    return temp

def num2expr(given):
    temp = Expr(Term(Num(given)))
    return temp

def expr2paren(given):
    temp = Expr(Term(Paren(given)))
    return temp

def multiply_factors2expr(given1, given2):
    temp = Expr(Term(given1, TermTail('*', Term(given2))))
    return temp
