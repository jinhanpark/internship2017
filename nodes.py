import math
import copy

class MetaExpr:
    def __init__(self, expr):
        self.expr

    def simplify(self):
        pass

    def __str__(self):
        return '%s'%str(self.expr)

class Empty:
    def __init__(self):
        pass

    def simplify(self):
        pass

    def __str__(self):
        return ''

class ExprCommon:
    def __init__(self, term, extail=Empty()):
        self.term = term
        self.extail = extail

    def simplify(self):
        self.term.simplify()
        self.extail.simplify()
        
        if isinstance(self, ExTail):
            self.remove_minus_op()

    def __neg__(self):
        new = copy.deepcopy(self)
        new.term = -new.term
        if not isinstance(new.extail, Empty):
            new.extail = -new.extail
        return new

    def __add__(self, another):
        return '%s+%s'%(str(self), str(another))

class Expr(ExprCommon):
    def __init__(self, term, extail=Empty()):
        ExprCommon.__init__(self, term, extail)

    def __str__(self):
        return '%s%s'%(str(self.term), str(self.extail))

class ExTail(ExprCommon):
    def __init__(self, op, term, extail=Empty()):
        ExprCommon.__init__(self, term, extail)
        self.op = op

    def remove_minus_op(self):
        if self.op == '-':
            self.op = '+'
            self.term = -self.term

    def __str__(self):
        return '%s%s%s'%(self.op, str(self.term), str(self.extail))

class TermCommon:
    def __init__(self, factor, termtail=Empty()):
        self.factor = factor
        self.termtail = termtail
        self.coeff = 1

    def simplify(self):
        self.factor.simplify()
        self.termtail.simplify()
        
        self.simplify_factor()

        if isinstance(self, TermTail):
            self.remove_div_op()
        else:
            self.get_coeff()
            self.remove_nums()

    def simplify_factor(self):
        self.factor = self.factor.simplified()

    def add_term_tail(self, given_termtail):
        assert isinstance(given_termtail, TermTail)
        if isinstance(self.termtail, Empty):
            self.termtail = given_termtail
        else:
            self.termtail.add_term_tail(given_termtail)

    def get_coeff(self):
        if not isinstance(self.termtail, Empty):
            self.termtail.get_coeff()
            self.coeff *= self.termtail.coeff
            self.termtail.coeff = 1
        self.coeff *= self.factor.coeff
        self.factor.coeff = 1

    def remove_nums(self):
        if not isinstance(self.termtail, Empty):
            self.termtail.remove_nums()
            if isinstance(self.termtail.factor, Num):
                self.termtail = self.termtail.termtail
            elif isinstance(self.factor, Num):
                self.factor = self.termtail.factor
                self.termtail = self.termtail.termtail

class Term(TermCommon):
    def __init__(self, factor, termtail=Empty()):        
        TermCommon.__init__(self, factor, termtail)

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

class TermTail(TermCommon):
    def __init__(self, op, factor, termtail=Empty()):
        TermCommon.__init__(self, factor, termtail)
        self.op = op

    def remove_div_op(self):
        if self.op == '/':
            self.op = '*'
            self.factor = self.factor.reciprocal()

    def __str__(self):
        return '%s%s%s'%(self.op, str(self.factor), str(self.termtail))

class Factor:
    def __init__(self, base, exp=1, coeff=1):
        self.coeff = coeff
        self.base = base
        self.exp = exp

    def reciprocal(self):
        new = copy.deepcopy(self)
        new.coeff = math.pow(self.coeff, -1)
        new.exp = -self.exp
        return new

    def __str__(self):
        coeff = self.coeff
        if coeff == 1:
            coeff_str = ''
        elif coeff == -1:
            coeff_str = '-'
        elif isinstance(self, Num):
            return '%.2f'%coeff
        else:
            coeff_str = '%.2f*'%coeff
        return '%spow(%s, %s)'%(coeff_str, str(self.base), str(self.exp))

class Pow(Factor):
    def __init__(self, base, exp, coeff=1):
        Factor.__init__(self, base, exp, coeff)

    def simplify(self):
        if not is_literal_expr(self.base):
            self.base.simplify()
        self.exp.simplify()

    def simplified(self):
        return Factor(self.base, self.exp, self.coeff)

class Literal(Factor):
    def __init__(self, value, coeff):
        Factor.__init__(self, value, coeff=coeff)

    def simplify(self):
        pass

    def simplified(self):
        return Factor(self.base)

    def __str__(self):
        return str(self.base)

class Var(Literal):
    def __init__(self, var, coeff=1):
        Literal.__init__(self, var, coeff)

class Const(Literal):
    def __init__(self, const, coeff=1):
        Literal.__init__(self, const, coeff)

class Num(Literal):
    def __init__(self, num, coeff=1):
        Literal.__init__(self, num, coeff)
        self.coeff *= float(self.base)
        self.base = 1

    def simplified(self):
        return self

    def reciprocal(self):
        new = copy.deepcopy(self)
        new.coeff = math.pow(self.coeff, -1)
        return new


class HaveExprInIt(Factor):
    def __init__(self, base, coeff):
        Factor.__init__(self, base, coeff=coeff)

    def simplify(self):
        self.base.simplify()
    
class SinVarFunc(HaveExprInIt):
    def __init__(self, expr, coeff=1):
        HaveExprInIt.__init__(self, expr, coeff)

    # def simplify(self):
    #     self.expr.simplify()

    def __str__(self):
        return '%s(%s)'%(self.func_name, str(self.expr))

class Paren(SinVarFunc): #regard Paren as identity function
    def __init__(self, expr, coeff=1):
        SinVarFunc.__init__(self, expr, coeff)
        self.func_name = ''


class Sin(SinVarFunc):
    def __init__(self, expr, coeff=1):
        SinVarFunc.__init__(self, expr, coeff)
        self.func_name = 'sin'


class Cos(SinVarFunc):
    def __init__(self, expr, coeff=1):
        SinVarFunc.__init__(self, expr, coeff)
        self.func_name = 'cos'


class Tan(SinVarFunc):
    def __init__(self, expr, coeff=1):
        SinVarFunc.__init__(self, expr, coeff)
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


class ArcSin(SinVarFunc):
    def __init__(self, expr, coeff=1):
        SinVarFunc.__init__(self, expr, coeff)
        self.func_name = 'arcsin'


class ArcCos(SinVarFunc):
    def __init__(self, expr, coeff=1):
        SinVarFunc.__init__(self, expr, coeff)
        self.func_name = 'arccos'


class ArcTan(SinVarFunc):
    def __init__(self, expr, coeff=1):
        SinVarFunc.__init__(self, expr, coeff)
        self.func_name = 'arctan'


class Log(SinVarFunc):
    def __init__(self, expr, coeff=1):
        SinVarFunc.__init__(self, expr, coeff)
        self.func_name = 'log'


def is_literal_expr(expr):
    extail = expr.extail
    termtail = expr.term.termtail
    factor = expr.term.factor
    return isinstance(extail, Empty) and\
        isinstance(termtail, Empty) and\
        isinstance(factor, Literal)


# def factor2expr(given):
#     temp = Expr(Term(given))
#     return temp

# def number2expr(given):
#     temp = Expr(Term(Num(given)))
#     temp.simplify()
#     return temp

# def expr2paren(given):
#     temp = Expr(Term(Paren(given)))
#     return temp

# def multiply_factors2expr(given1, given2):
#     temp = Expr(Term(given1, TermTail('*', Term(given2))))
#     return temp
