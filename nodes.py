import math
import copy

class Empty:
    def __init__(self):
        pass

    def simplify(self):
        pass

    def __str__(self):
        return ''

class MetaExpr:
    def __init__(self, term, extail=Empty()):
        self.term = term
        self.extail = extail

    def __neg__(self):
        new = copy.deepcopy(self)
        new.term = -new.term
        if not isinstance(new.extail, Empty):
            new.extail = -new.extail
        return new

    def __add__(self, another):
        return '%s+%s'%(str(self), str(another))

class Expr(MetaExpr):
    def __init__(self, term, extail=Empty()):
        MetaExpr.__init__(self, term, extail)

    def simplify(self):
        self.term.simplify()
        self.extail.simplify()

    # def simplify_term(self):
    #     self.term.simplify_hidden_expr()
    #     self.term.powerize()
    #     self.term.get_coeff()
    #     self.term.remove_nums()

    def __str__(self):
        return '%s%s'%(str(self.term), str(self.extail))

class ExTail(MetaExpr):
    def __init__(self, op, term, extail=Empty()):
        MetaExpr.__init__(self, term, extail)
        self.op = op

    def simplify(self):
        self.remove_minus_op()
        self.term.simplify()
        self.extail.simplify()

    def remove_minus_op(self):
        if self.op == '-':
            self.op = '+'
            self.term = -self.term

    def __str__(self):
        return '%s%s%s'%(self.op, str(self.term), str(self.extail))

class MetaTerm:
    def __init__(self, factor, termtail=Empty()):
        self.factor = factor
        self.termtail = termtail

    def add_term_tail(self, given_termtail):
        assert isinstance(given_termtail, TermTail)
        if isinstance(self.termtail, Empty):
            self.termtail = given_termtail
        else:
            self.termtail.add_term_tail(given_termtail)

class Term(MetaTerm):
    def __init__(self, factor, termtail=Empty()):        
        MetaTerm.__init__(self, factor, termtail)
        self.coeff = 1

    def simplify(self):
        pass
    #     self.factor.simplify()
    #     self.termtail.simplify()

    # def powerize(self, ind=1):
    #     self.factor = self.factor.powerized(ind)
    #     if not isinstance(self.termtail, Empty):
    #         if self.termtail.op == '/':
    #             self.termtail.op  = '*'
    #             ind = -1
    #         self.termtail.term.powerize(ind)

    # def get_coeff(self):
    #     self.coeff *= self.factor.coeff
    #     self.factor.coeff = 1
    #     if not isinstance(self.termtail, Empty):
    #         self.termtail.term.get_coeff()
    #         self.coeff *= self.termtail.term.coeff
    #         self.termtail.term.coeff = 1

    # def remove_nums(self):
    #     self.remove_right_nums()
    #     self.remove_left_num()

    # def remove_right_nums(self):
    #     if not isinstance(self.termtail, Empty):
    #         if isinstance(self.termtail.term.factor, Num): # remove tail nums
    #             self.termtail.term.remove_right_nums()
    #             self.termtail = self.termtail.term.termtail
    #         else:
    #             self.termtail.term.remove_right_nums()

    # def remove_left_num(self):
    #     if isinstance(self.factor, Num) and\
    #        not isinstance(self.termtail, Empty): # remove last first num if it has nonempty tail
    #         self.factor = self.termtail.term.factor
    #         self.termtail = self.termtail.term.termtail


    def __str__(self):
        coeff = self.coeff
        coeff_str = '%.2f*'%coeff
        if coeff == 1:
            coeff_str = ''
        elif coeff == -1:
            coeff_str = '-'
        elif isinstance(self.factor, Num):
            coeff_str = '%.2f'%coeff
            if isinstance(self.termtail, Empty):
                return coeff_str
            else:
                return '%s%s'%(coeff_str, str(self.termtail))
        return '%s%s%s'%(coeff_str, str(self.factor), str(self.termtail))

    def __neg__(self):
        new = copy.deepcopy(self)
        new.coeff *= -1
        return new

class TermTail(MetaTerm):
    def __init__(self, op, factor, termtail=Empty()):
        MetaTerm.__init__(self, factor, termtail)
        self.op = op

    # def simplify(self):
    #     self.factor.simplify()
    #     self.termtail.simplify()

    def __str__(self):
        return '%s%s%s'%(self.op, str(self.factor), str(self.termtail))

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

    # def simplify(self):
    #     self.base.simplify()
    #     self.ind.simplify()

    # def powerized(self, ind=1):
    #     if ind == -1:
    #         self.ind = -self.ind
    #     return self


    def __str__(self):
        return 'pow(%s, %s)'%(str(self.base), str(self.ind))

class Var(Factor):
    def __init__(self, var, coeff = 1):
        Factor.__init__(self, coeff)
        self.var = var


    def __str__(self):
        return str(self.var)

class Const(Factor):
    def __init__(self, const, coeff = 1):
        Factor.__init__(self, coeff)
        self.const = const


    def __str__(self):
        return str(self.const)

class Num(Factor):
    def __init__(self, num, coeff = 1):
        Factor.__init__(self, coeff)
        self.coeff *= float(num)
        self.num = 1

    # def powerized(self, ind=1):
    #     self.coeff = math.pow(self.coeff, ind)
    #     return self


    def __str__(self):
        # if self.num == 1: #delete *1's
        #     return '\b'
        return str(self.coeff)

class SingleFunction(Factor):
    def __init__(self, expr, coeff=1):
        Factor.__init__(self, coeff)
        self.expr = expr

    # def simplify(self):
    #     self.expr.simplify()

    def __str__(self):
        return '%s(%s)'%(self.func_name, str(self.expr))

class Paren(SingleFunction): #regard Paren as identity function
    def __init__(self, expr, coeff=1):
        SingleFunction.__init__(self, expr, coeff)
        self.func_name = ''


class Sin(SingleFunction):
    def __init__(self, expr, coeff=1):
        SingleFunction.__init__(self, expr, coeff)
        self.func_name = 'sin'


class Cos(SingleFunction):
    def __init__(self, expr, coeff=1):
        SingleFunction.__init__(self, expr, coeff)
        self.func_name = 'cos'


class Tan(SingleFunction):
    def __init__(self, expr, coeff=1):
        SingleFunction.__init__(self, expr, coeff)
        self.func_name = 'tan'

    # def powerized(self, ind):        
    #     sin_ind = number2expr(ind)
    #     cos_ind = number2expr(-ind)
    #     self.expr.powerize()
    #     sin = factor2expr(Sin(self.expr))
    #     cos = factor2expr(Cos(self.expr))
    #     expr = multiply_factors2expr(Pow(sin, sin_ind),
    #                                  Pow(cos, cos_ind))
    #     return Paren(expr, self.coeff)


class ArcSin(SingleFunction):
    def __init__(self, expr, coeff=1):
        SingleFunction.__init__(self, expr, coeff)
        self.func_name = 'arcsin'


class ArcCos(SingleFunction):
    def __init__(self, expr, coeff=1):
        SingleFunction.__init__(self, expr, coeff)
        self.func_name = 'arccos'


class ArcTan(SingleFunction):
    def __init__(self, expr, coeff=1):
        SingleFunction.__init__(self, expr, coeff)
        self.func_name = 'arctan'


class Log(SingleFunction):
    def __init__(self, expr, coeff=1):
        SingleFunction.__init__(self, expr, coeff)
        self.func_name = 'log'


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
