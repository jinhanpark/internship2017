import math

class Empty:
    def __init__(self):
        pass

    def is_empty(self):
        return True

    def __str__(self):
        return ''

class Expr:
    def __init__(self, term, extail=Empty()):
        self.term = term
        self.extail = extail

    def simplify(self):
        pass

    def eval(self):
        pass

    def __str__(self):
        return str(self.term) + str(self.extail)

class ExTail:
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

    def is_empty(self):
        return False

    def __str__(self):
        return str(self.op) + str(self.expr)

class Term:
    def __init__(self, factor, termtail=Empty()):
        self.factor = factor
        self.termtail = termtail
        self.coeff = self.get_coeff()

    def simplify(self):
        pass

    def eval(self):
        pass

    def get_coeff(self):
        if self.termtail.is_empty():
            return self.factor.coeff
        else:
            return self.factor.coeff * self.termtail.term.coeff

    def __str__(self):
        return '%s%s'%(str(self.factor),str(self.termtail))

class TermTail:
    def __init__(self, op, term):
        self.op = op
        self.term = term

    def is_empty(self):
        return False

    def __str__(self):
        return str(self.op) + str(self.term)

class Factor:
    def __init__(self, coeff):
        self.coeff = coeff

class SingleFunction(Factor):
    def __init__(self, expr, coeff=1):
        Factor.__init__(self, coeff)
        self.expr = expr
        self.func_name = ''
        if coeff == 1:
            self.sign = ''
        else:
            self.sign = '-'

    def __str__(self):
        return '%s%s(%s)'%(self.sign, self.func_name, str(self.expr))

class Paren(SingleFunction): #regard Paren as identity function
    def __init__(self, expr, coeff=1):
        SingleFunction.__init__(self, expr, coeff)

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
        self.base = base
        self.ind = ind
        self.func_name = 'pow'
        if coeff == 1:
            self.sign = ''
        else:
            self.sign = '-'

    def eval(self):
        pass

    def __str__(self):
        return '%spow(%s, %s)'%(self.sign, str(self.base), str(self.ind))

class Num():
    def __init__(self, num, coeff = 1):
        self.num = float(num) * coeff
        self.coeff = self.num

    def eval(self):
        pass

    def __str__(self):
        return str(self.num)
