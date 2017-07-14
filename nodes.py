import math
import copy

def is_num(x):
    return type(x) == int or type(x) == float

def factor2expr(given):
    copied = copy.deepcopy(given)
    new = Expr(Term(copied))
    return new

def num2expr(given):
    if isinstance(given, Expr):
        assert given.is_single_factor(Num)
        return given
    else:
        copied = copy.deepcopy(given)
        new = Expr(Term(Num(copied)))
        return new

# def expr2paren(given):
#     temp = Expr(Term(Paren(given)))
#     return temp

# def multiply_factors2expr(given1, given2):
#     temp = Expr(Term(given1, TermTail('*', Term(given2))))
#     return temp

class Empty:
    def __init__(self):
        pass

    def simplify(self):
        pass

    def __repr__(self):
        return str(self)

    def __str__(self):
        return ''

    def __add__(self):
        pass

class Factor:
    def __init__(self, base, exp=1.0, coeff=1.):
        self.coeff = coeff
        self.base = base
        self.exp = exp

    def reciprocal(self):
        new = copy.deepcopy(self)
        new.coeff = math.pow(self.coeff, -1)
        if is_num(self.exp):
            new.exp = num2expr(-self.exp)
        else:
            new.exp = -self.exp
        return new

    def __repr__(self):
        return str(self)

    def __str__(self):
        coeff_str = ''
#        coeff_str = 'fact%f*'%self.coeff
        return '%spow(%s, %s)'%(coeff_str, str(self.base), str(self.exp))

    def __lt__(self, another):
        assert isinstance(another, Factor)
        return str(self.base) < str(another.base)

    def __eq__(self, another):
        assert isinstance(another, Factor)
        return str(self.base) == str(another.base)

    def __le__(self, another):
        return self < another or self == another

class Pow(Factor):
    def __init__(self, base, exp, coeff=1.):
        Factor.__init__(self, base, exp, coeff)
        assert isinstance(base, Expr)
        assert isinstance(exp, Expr)

    def penetrate(self):
        self.base.simplify()

    def simplified(self):
        self.exp = self.exp.simplified()
        if isinstance(self.base.extail, Empty):
            if isinstance(self.base.term.termtail, Empty): # when single factor
                inner_factor = self.base.term.factor
                if isinstance(inner_factor, Pow):
                    return Pow(inner_factor.base, self.exp*inner_factor.exp)
                self.base.penetrate()
                inner_factor = self.base.term.factor
                if isinstance(inner_factor, Paren):
                    return Pow(inner_factor.base, self.exp*inner_factor.exp)
                elif isinstance(inner_factor, Num) and\
                     self.exp.is_single_factor(Num):
                    return Num(math.pow(self.base.term.coeff, self.exp.term.coeff))
                else:
                    return self
            else: # when single term
                self.base.term.power_by(self.exp)
                return Paren(self.base.simplified())
        else: # when have extail
            self.base = self.base.simplified()
            if self.base.term.coeff != 1:
                new = Expr(Term(Num(self.base.term.coeff), TermTail('*', Paren(self.base.monic()))))
                return Pow(new, self.exp)
            elif self.exp.is_single_factor(Num) and\
               self.exp.term.coeff == int(self.exp.term.coeff) and\
               self.exp.term.coeff > 1:
                new = num2expr(1)
                while self.exp.term.coeff > 0:
                    new *= self.base
                    self.exp.term.coeff -= 1
                return Paren(new)
            else:
                return self

        # if self.base.is_single_factor():
        #     self.base.penetrate()
        # else:
        #     self.base.simplify()
        # return self

class Literal(Factor):
    def __init__(self, value, coeff=1.):
        Factor.__init__(self, value, coeff=coeff)

    def penetrate(self):
        pass

    def simplified(self):
        return Pow(factor2expr(self), num2expr(self.exp))

    def __repr__(self):
        return str(self)

    def __str__(self):
        coeff_str = ''
#        coeff_str = 'literal%f*'%self.coeff
        return '%s%s'%(coeff_str, str(self.base))

class Var(Literal):
    def __init__(self, var, coeff=1.):
        Literal.__init__(self, var, coeff)

class Const(Literal):
    def __init__(self, const, coeff=1.):
        Literal.__init__(self, const, coeff)

class Num(Literal):
    def __init__(self, num, coeff=1.):
        Literal.__init__(self, num, coeff)
        self.coeff *= float(self.base)
        self.base = 1

    def simplified(self):
        return self

    def reciprocal(self):
        new = copy.deepcopy(self)
        new.coeff = math.pow(self.coeff, -1)
        return new

    # def __str__(self):
    #     return '%f'%self.base

class SinVarFunc(Factor):
    def __init__(self, expr, coeff=1.):
        Factor.__init__(self, expr, coeff)

    def penetrate(self):
        self.base.simplify()

    def simplified(self):
        self.base.simplify()
        return Pow(factor2expr(self), num2expr(self.exp))

    def __repr__(self):
        return str(self)

    def __str__(self):
        coeff_str = ''
#        coeff_str = 'fact%f*'%self.coeff
        return '%s%s(%s)'%(coeff_str, self.func_name, str(self.base))

class Paren(SinVarFunc): #regard Paren as identity function
    def __init__(self, expr, coeff=1.):
        SinVarFunc.__init__(self, expr, coeff)
        self.func_name = ''

    def simplified(self):
        if self.base.is_single_factor():
            self.base.penetrate()
            new = copy.deepcopy(self.base.term.factor)
            new.coeff *= self.base.term.coeff
            new.exp = self.exp*new.exp
            return new
        elif self.exp == 1:
            self.base.simplify()
            return self
        else:
            self.base.simplify()
            return Pow(self.base, self.exp)


class Sin(SinVarFunc):
    def __init__(self, expr, coeff=1.):
        SinVarFunc.__init__(self, expr, coeff)
        self.func_name = 'sin'


class Cos(SinVarFunc):
    def __init__(self, expr, coeff=1.):
        SinVarFunc.__init__(self, expr, coeff)
        self.func_name = 'cos'


class Tan(SinVarFunc):
    def __init__(self, expr, coeff=1.):
        SinVarFunc.__init__(self, expr, coeff)
        self.func_name = 'tan'

    def simplified(self):
        sin_ind = num2expr(self.exp)
        cos_ind = num2expr(-self.exp)
        self.base.simplify()
        sin = Pow(factor2expr(Sin(self.base)), sin_ind)
        cos = Pow(factor2expr(Cos(self.base)), cos_ind)
        new = Expr(Term(sin, TermTail('*', cos)))
        return Paren(new)

class Log(SinVarFunc):
    def __init__(self, expr, coeff=1.):
        SinVarFunc.__init__(self, expr, coeff)
        self.func_name = 'log'

class TermCommon:
    def __init__(self, factor, termtail=Empty(), coeff=1.):
        self.factor = factor
        self.termtail = termtail
        self.coeff = coeff
        self.remove_div_op()
        self.get_coeff()

    def simplify(self):
        #before
        # if isinstance(self, TermTail): #may not need this
        #     self.termtail.remove_div_op()
        self.remove_left_nums()
        self.factor = self.factor.simplified()
        
        #recursion
        self.termtail.simplify()

        #after
        self.get_coeff()
        self.remove_right_most_num()
        self.order_and_gather_factors()
        self.unparenize_term()
        self.zero_exp_factor_to_one()

    def remove_div_op(self):
        if isinstance(self, TermTail) and self.op == '/':
            self.op = '*'
            self.factor = self.factor.reciprocal()

    def get_coeff(self):
        if isinstance(self.termtail, TermTail):
            self.coeff *= self.termtail.coeff
            self.termtail.coeff = 1.
        self.coeff *= self.factor.coeff
        self.factor.coeff = 1.

    def remove_left_nums(self):
            while isinstance(self.factor, Num) and\
                  isinstance(self.termtail, TermTail):
                self.coeff *= self.factor.coeff
                self.factor = self.termtail.factor
                self.termtail = self.termtail.termtail

    def remove_right_most_num(self):
        if isinstance(self.termtail, TermTail):
            if isinstance(self.termtail.factor, Num):
                self.termtail = self.termtail.termtail

    def order_and_gather_factors(self):
        if isinstance(self.termtail, TermTail):
            self.termtail.order_and_gather_factors()
            if self.factor < self.termtail.factor:
                self.factor, self.termtail.factor = self.termtail.factor, self.factor
            elif isinstance(self.factor, Paren):
                pass
            elif self.factor == self.termtail.factor:
                self.factor.exp += self.termtail.factor.exp
                self.termtail = self.termtail.termtail

    def unparenize_term(self):
        if isinstance(self.termtail, TermTail):
            if isinstance(self.termtail.factor, Paren) and\
               self.termtail.factor.exp == 1:
                self.factor = Paren(self.termtail.factor.base * self.factor)
                self.termtail = self.termtail.termtail
            elif isinstance(self.factor, Paren) and\
                 self.factor.exp == 1:
                self.factor = Paren(self.factor.base * self.termtail)
                self.termtail = Empty()

    def zero_exp_factor_to_one(self):
        if self.factor.exp == 0:
            self.factor = Num(1)

    def power_by(self, exp):
        if self.coeff != 1:
            new_factor = Num(self.coeff)
            self.coeff = 1.
            self.termtail = self.tailized()
            self.factor = new_factor
        self.factor = Pow(factor2expr(self.factor), exp).simplified()
        if isinstance(self.termtail, TermTail):
            self.termtail.power_by(exp)

    def tailized(self):
        return TermTail('*', self.factor, self.termtail, self.coeff)

    def add_termtail(self, given_termtail):
        assert isinstance(given_termtail, TermTail)
        self.coeff *= given_termtail.coeff
        given_termtail.coeff = 1.
        if isinstance(self.termtail, Empty):
            self.termtail = given_termtail
        else:
            self.termtail.add_termtail(given_termtail)


class Term(TermCommon):
    def __init__(self, factor, termtail=Empty(), coeff=1.):        
        TermCommon.__init__(self, factor, termtail, coeff)

    def is_single_factor(self, instance=Factor):
        tail_check = isinstance(self.termtail, Empty)
        factor_check = isinstance(self.factor, instance)
        return tail_check and factor_check

    def __repr__(self):
        return str(self)

    def __str__(self):
        if isinstance(self, TermTail):
            op_str = self.op
        else:
            op_str = ''
        factor_str = str(self.factor)
        termtail_str = str(self.termtail)
        coeff_str = ''
        # coeff = self.coeff #for debug
        # if coeff == 1:
        #     coeff_str = ''
        # elif coeff == -1:
        #     coeff_str = '-'
        # else:
        #     coeff_str = 'term%f*'%coeff #end for debug
        return '%s%s%s%s'%(op_str, coeff_str, factor_str, termtail_str)

    def __mul__(self, another):
        assert isinstance(another, Factor) or\
            isinstance(another, Term) or\
            isinstance(another, Expr) or\
            isinstance(another, float) or\
            isinstance(another, int)

        new = copy.deepcopy(self)
        if isinstance(another, Factor):
            return Term(another) * new
        elif isinstance(another, Term):
            new.add_termtail(another.tailized())
            return new
        elif isinstance(another, Expr):
            return another * new
        else:
            new.coeff *= another
            return new

    def __neg__(self):
        new = copy.deepcopy(self)
        new.coeff *= -1
        return new

    def __lt__(self, another):
        assert isinstance(another, Term)
        return str(self) < str(another)

    def __eq__(self, another):
        assert isinstance(another, Term)
        return str(self) == str(another)

    def __le__(self, another):
        return self < another or self == another


class TermTail(TermCommon):
    def __init__(self, op, factor, termtail=Empty(), coeff=1.):
        self.op = op
        TermCommon.__init__(self, factor, termtail, coeff)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '%s%s%s'%(self.op, str(self.factor), str(self.termtail))

class ExprCommon:
    def __init__(self, term, extail=Empty()):
        self.term = term
        self.extail = extail
        self.remove_minus_op()

    def simplify(self):
        #before recursion : left to right propagation
        # if isinstance(self, ExTail): #may not need this
        #     self.remove_minus_op()
        self.term.simplify()
        self.unparenize_expr()

        #recursion step
        self.extail.simplify()
        
        #after recursion : right to left propagation
        self.order_and_gather_terms()
        self.remove_zero_term()

    def remove_minus_op(self):
        if isinstance(self, ExTail) and self.op == '-':
            self.op = '+'
            self.term *= -1

    def unparenize_expr(self):
        if self.term.is_single_factor(Paren) and\
           self.term.factor.exp == 1:
            expr = self.term.factor.base
            expr *= self.term.coeff
            expr.add_extail(self.extail)
            self.term = expr.term
            self.extail = expr.extail

    def order_and_gather_terms(self): #idea from bubble sort
        if isinstance(self.extail, ExTail):
            self.extail.order_and_gather_terms()
            if self.term < self.extail.term:
                self.term, self.extail.term = self.extail.term, self.term
            elif self.term == self.extail.term:
                self.term.coeff += self.extail.term.coeff
                self.extail = self.extail.extail
                if self.term.coeff == 0:
                    self.term = Term(Num(0))

    def remove_zero_term(self):
        if isinstance(self.extail, ExTail):
            if self.extail.term.coeff == 0:
                self.extail = self.extail.extail

    def add_extail(self, given_extail):
        assert isinstance(given_extail, ExTail) or isinstance(given_extail, Empty)
        if isinstance(given_extail, Empty):
            pass
        elif isinstance(self.extail, Empty):
            self.extail = given_extail
        else:
            self.extail.add_extail(given_extail)

    def monic(self, div_factor=1.):
        if isinstance(self, Expr):
            new = copy.deepcopy(self)
            div_factor = self.term.coeff
        else:
            new = self
        new.term.coeff /= div_factor
        if isinstance(new.extail, ExTail):
            new.extail = new.extail.monic(div_factor)
        return new

    def __repr__(self):
        return str(self)

    def __str__(self):
        if isinstance(self, ExTail):
            op_str = self.op
        else:
            op_str = ''
        term_str = str(self.term)
        extail_str = str(self.extail)
        coeff = self.term.coeff
        coeff_str = '%f*'%coeff
        if coeff == 1:
            coeff_str = ''
        elif coeff == -1:
            coeff_str = '-'
        elif isinstance(self.term.factor, Num):
            coeff_str = '%f'%coeff
            term_str = str(self.term.termtail)
        return '%s%s%s%s'%(op_str, coeff_str, term_str, extail_str)

    def __eq__(self, another):
        if is_num(another):
            another_str = str(MetaExpr(Expr(Term(Num(another)))))
        else:
            another_str = str(another)
        return str(self) == another_str

    def __neg__(self):
        new = copy.deepcopy(self)
        new.term = -new.term
        if isinstance(new.extail, ExTail):
            new.extail = -new.extail
        return new

    def __add__(self, another):
        assert isinstance(another, Expr)
        new = copy.deepcopy(self)
        new.add_extail(another.tailized())
        new.simplify()
        return new

    def __mul__(self, another):
        assert isinstance(another, Factor) or\
            isinstance(another, TermCommon) or\
            isinstance(another, Expr) or\
            isinstance(another, float) or\
            isinstance(another, int)
        
        if isinstance(self, Expr):
            new = copy.deepcopy(self)
        else:
            new = self

        if isinstance(another, Factor):
            new.term *= another
        elif isinstance(another, TermCommon):
            new.term.add_termtail(another.tailized())
        elif isinstance(another, Expr):
            new.term = Term(Paren(new.term*another))
        else:
            new.term *= another
        if isinstance(self.extail, ExTail):
            new.extail *= another
        new.simplify()
        return new

class Expr(ExprCommon):
    def __init__(self, term, extail=Empty()):
        ExprCommon.__init__(self, term, extail)

    def penetrate(self):#have to deal with this
        self.term.factor.penetrate()

    def simplified(self):
        new = copy.deepcopy(self)
        return MetaExpr(new).expr

    def is_single_factor(self, instance = Factor):
        extail_check = isinstance(self.extail, Empty)
        termtail_check = isinstance(self.term.termtail, Empty)
        if instance != 0:
            factor_check = isinstance(self.term.factor, instance)
        else:
            factor_check = isinstance(self.term.factor)
        return extail_check and termtail_check and factor_check

    def tailized(self):
        return ExTail('+', self.term, self.extail)

class ExTail(ExprCommon):
    def __init__(self, op, term, extail=Empty()):
        self.op = op
        ExprCommon.__init__(self, term, extail)

class MetaExpr:
    def __init__(self, given):
        if isinstance(given, Expr):
            self.expr = given
        elif isinstance(given, Term):
            self.expr = Expr(given)
        elif isinstance(given, Factor):
            self.expr = Expr(Term(given))
        elif is_num(given):
            self.expr = Expr(Term(Num(given)))
        else:
            raise ValueError
        self.simplify()

    def simplify(self):
        before = 'before'
        after = str(self.expr)
        while before != after:
            self.expr.simplify()
            before = after
            after = str(self.expr)
        return self

    def __eq__(self, another):
        return self.expr == another

    def __neg__(self):
        return MetaExpr(-self.expr)

    def __add__(self, another):
        if isinstance(another, MetaExpr):
            return MetaExpr(self.expr + another.expr)
        else:
            return MetaExpr(self.expr + another)

    def __mul__(self, another):
        if isinstance(another, MetaExpr):
            return MetaExpr(self.expr * another.expr)
        else:
            return MetaExpr(self.expr * another)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '%s'%str(self.expr)
