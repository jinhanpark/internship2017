import math
import numpy as np
from copy import deepcopy

def is_num(x):
    return type(x) == int or type(x) == float

def is_int_expr(expr):
    check_Num = expr.is_single_factor(Num)
    check_int = int(expr.term.coeff) == float(expr.term.coeff)
    return check_int and check_Num

def no_var_in_str(s):
    return (not 'x' in s) and (not 'y' in s)

def factor2expr(given):
    copied = deepcopy(given)
    new = Expr(Term(copied))
    return new

def num2expr(given):
    if isinstance(given, Expr):
        assert given.is_single_factor(Num)
        return given
    else:
        copied = deepcopy(given)
        new = Expr(Term(Num(copied)))
        return new


class Empty:
    def __init__(self):
        self.term = ''
#        self.extail = self

    def simplify(self): # may be no need
        pass

    def child_simplify(self):
        pass

    def unparenize(self):
        pass

    def sort(self):
        pass

    def gather(self):
        pass

    def remove_zeros(self):
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
        if isinstance(exp, Expr):
            self.exp = exp
        else:
            self.exp = num2expr(exp)

    def reciprocal(self):
        new = deepcopy(self)
        new.coeff = math.pow(self.coeff, -1)
        if is_num(self.exp):
            new.exp = num2expr(-self.exp)
        else:
            new.exp = -self.exp
        return new

    def __repr__(self):
        return str(self)

    def __lt__(self, another):
        assert isinstance(another, Factor)
        self_num, another_num = isinstance(self, Num), isinstance(another, Num)
        if not self_num and another_num:
            return True
        elif self_num and not another_num:
            return False
        elif self_num and another_num:
            return False
        else: # both not num
            if str(self.base) < str(another.base):
                return True
            elif str(self.base) > str(another.base):
                return False
            else: #same base
                self_exp_num, another_exp_num = self.exp.is_single_factor(Num), another.exp.is_single_factor(Num)
                if not self_exp_num and another_exp_num:
                    return True
                elif self_exp_num and not another_exp_num:
                    return False
                elif self_exp_num and another_exp_num:
                    self_exp_int, another_exp_int = is_int_expr(self.exp), is_int_expr(another.exp)
                    if not self_exp_int and another_exp_int:
                        return True
                    elif self_exp_int and not another_exp_int:
                        return False
                    else:
                        return self.exp.term.coeff < another.exp.term.coeff
                else:
                    return str(self.exp) < str(another.exp)

    def __eq__(self, another):
        assert isinstance(another, Factor)
        return str(self.base) == str(another.base)
        return str(self) == str(another)

    def __le__(self, another):
        return self<another or self == another

class Pow(Factor):
    def __init__(self, base, exp, coeff=1.):
        Factor.__init__(self, base, exp, coeff)
        assert isinstance(base, Expr)
        assert isinstance(exp, Expr)

    def penetrate(self):
        self.base.simplify()

    def simplified(self):
        self.exp = self.exp.simplified()
        while self.base.is_single_factor(Pow) and\
              self.base.term.coeff == 1 and\
              ((is_int_expr(self.exp) and is_int_expr(self.base.term.factor.exp)) or\
               self.exp == 1 or self.base.term.factor.exp == 1):
            self.exp = self.exp*self.base.term.factor.exp
            self.base = self.base.term.factor.base
        if self.base.is_single_factor(Num) and\
           self.exp.is_single_factor(Num):
            return Num(pow(self.base.term.coeff, self.exp.term.coeff))
        elif self.base.is_single_factor(Pow) and\
             self.base.term.coeff == 1:
            self.base = self.base.simplified()
            return self
        elif isinstance(self.base.extail, ExTail):
            self.base = self.base.simplified()
            if self.base.term.coeff != 1:
                new = Expr(Term(Num(self.base.term.coeff), TermTail('*', Paren(self.base.monic()))))
                return Pow(new, self.exp)
            elif self.exp.is_single_factor(Num) and\
                 self.exp.term.coeff > 0 and\
                 self.exp.term.coeff == int(self.exp.term.coeff):
                new = num2expr(1)
                while self.exp.term.coeff > 0:
                    new *= self.base
                    self.exp.term.coeff -= 1
                return Paren(new)
            else:
                return self
        elif isinstance(self.base.term.termtail, TermTail) or\
             (self.base.term.coeff != 1 and not self.base.is_single_factor(Num)):
            self.base.term.power_by(self.exp)
            return Paren(self.base.simplified())
        else:
            before_base = deepcopy(self.base)
            before_factor = before_base.term.factor
            self.base.penetrate()
            inner_factor = self.base.term.factor
            if isinstance(inner_factor, Paren):
                return Pow(inner_factor.base, self.exp*inner_factor.exp)
            elif isinstance(inner_factor, Num) and\
                 self.exp.is_single_factor(Num):
                return Num(math.pow(self.base.term.coeff, self.exp.term.coeff))
            elif isinstance(inner_factor, Log) and\
                 str(inner_factor.base.term.factor.base) == 'e':
                return Pow(inner_factor.base.term.factor.exp, self.exp)
            elif isinstance(inner_factor, Tan):
                self.base = self.base.simplified()
                return self
            else:
                return self
 
    def __str__(self):
        return 'pow(%s, %s)'%(str(self.base), str(self.exp))

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
        return str(self.base)

class Var(Literal):
    def __init__(self, var, coeff=1.):
        Literal.__init__(self, var, coeff)

class Const(Literal):
    def __init__(self, const, coeff=1.):
        Literal.__init__(self, const, coeff)

class Num(Literal):
    def __init__(self, num, coeff=1.):
        self.coeff = coeff
        self.base = num
        self.exp = 1.
        self.coeff *= float(self.base)
        self.base = 1

    def simplified(self):
        return self

    def reciprocal(self):
        new = deepcopy(self)
        new.coeff = math.pow(self.coeff, -1)
        return new

class SinVarFunc(Factor):
    def __init__(self, expr, coeff=1.):
        Factor.__init__(self, expr, coeff=coeff)

    def penetrate(self):
        self.base.simplify()

    def simplified(self):
        self.base.simplify()
        new_exp = num2expr(self.exp)
        self.exp = num2expr(1)
        new_base = factor2expr(self)
        return Pow(new_base, new_exp)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '%s(%s)'%(self.func_name, str(self.base))

class Paren(SinVarFunc): #regard Paren as identity function
    def __init__(self, expr, coeff=1.):
        self.func_name = ''
        SinVarFunc.__init__(self, expr, coeff)

    def simplified(self):
        while isinstance(self.base, Expr) and\
              self.base.is_single_factor(Paren):
            self.coeff *= self.base.term.coeff
            self.exp *= self.base.term.factor.exp
            self.base = self.base.term.factor.base
        if self.base.is_single_factor(Factor):
            self.base.penetrate()
            new = deepcopy(self.base.term.factor)
            new.coeff *= self.base.term.coeff
            new.exp = self.exp * new.exp
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
        self.func_name = 'log'
        SinVarFunc.__init__(self, expr, coeff)
        assert self.exp == 1

    def simplified(self):
        outer_exp = self.exp.simplified()
        self.exp = num2expr(1)
        if self.base.is_single_factor(Num):
            return Pow(num2expr(math.log(self.base.term.coeff)), outer_exp)
        if isinstance(self.base.extail, ExTail):
            self.base = self.base.simplified()
            if self.base.term.coeff != 1:
                new = Expr(Term(Num(math.log(self.base.term.coeff))),
                           ExTail('+', Term(Log(self.base.monic))))
                return Pow(factor2expr(Paren(new)), outer_exp)
            else:
                return Pow(factor2expr(self), outer_exp)
        elif isinstance(self.base.term.termtail, TermTail) or\
             self.base.term.coeff != 1:
            new = self.base.term.log_distributed()
            return Pow(new, outer_exp)
        else:
            inner_factor = self.base.term.factor
            if inner_factor.exp != 1:
                exp_backup = inner_factor.exp
                inner_factor.exp = num2expr(1)
                new = Expr(Term(Paren(exp_backup), TermTail('*', self)))
                return Pow(new, outer_exp)
            elif isinstance(inner_factor, Const) and\
                 str(self.base) == 'e':
                    return Num(1)
            elif isinstance(inner_factor, Pow):
                return Log(inner_factor.base)
            else:
                return Pow(factor2expr(self), outer_exp)


class TermCommon:
    def __init__(self, factor, termtail=Empty(), coeff=1.):
        self.factor = factor
        self.termtail = termtail
        self.coeff = coeff
        self.remove_div_op()
        self.get_coeff()

    def simplify(self):
        #before
        self.remove_left_nums()
        self.simplify_factor()
        
        #recursion
        self.termtail.simplify()

        #after
        self.get_coeff()
        self.remove_right_most_num()
        self.order_and_gather_factors()
        self.unparenize_term()
        self.zero_exp_factor_to_one()
        if isinstance(self, Term):
            self.gather_pows_with_same_exp()

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

    def simplify_factor(self):
        before = 'before'
        after = str(self.factor)
        while before != after:
            self.coeff *= self.factor.coeff
            self.factor.coeff = 1
            self.factor = self.factor.simplified()
            before = after
            after = str(self.factor)

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
                if (is_int_expr(self.factor.exp) and is_int_expr(self.termtail.factor.exp) and self.factor.exp.term.coeff * self.termtail.factor.exp.term.coeff > 0) or\
                   no_var_in_str(str(self.factor.base)):
                    self.factor.exp += self.termtail.factor.exp
                    self.termtail = self.termtail.termtail

    def gather_pows_with_same_exp(self):
        traveler_before = self
        traveler = self.termtail
        while isinstance(traveler, TermTail):
            if isinstance(self.factor, Pow) and\
               isinstance(traveler.factor, Pow) and\
               self.factor.exp == traveler.factor.exp and\
               (isinstance(self.factor.base.extail, ExTail) or\
                isinstance(traveler.factor.base.extail, ExTail)):
                self.factor.base = self.factor.base * traveler.factor.base
                self.factor.base.simplify()
                traveler = traveler.termtail
                traveler_before.termtail = traveler
            else:
                traveler_before = traveler
                traveler = traveler.termtail
                

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

    def log_distributed(self):
        if self.coeff != 1:
            new_factor = Num(self.coeff)
            self.coeff = 1.
            self.termtail = self.tailized()
            self.factor = new_factor
        
        new_term = Term(Log(factor2expr(self.factor)))
        if isinstance(self.termtail, TermTail):
            new_extail = self.termtail.log_distributed()
        else:
            new_extail = Empty()
    
        if isinstance(self, Term):
            return Expr(new_term, new_extail)
        elif isinstance(self, TermTail):
            return ExTail('+', new_term, new_extail)
            

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
        return '%s%s%s'%(op_str, factor_str, termtail_str)

    def __mul__(self, another):
        assert isinstance(another, Factor) or\
            isinstance(another, Term) or\
            isinstance(another, Expr) or\
            isinstance(another, float) or\
            isinstance(another, int)
        new = deepcopy(self)
        another = deepcopy(another)
        
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
        new = deepcopy(self)
        new.coeff *= -1
        return new

    def __lt__(self, another):
        assert isinstance(another, Term)
        return str(self) < str(another)

    def __eq__(self, another):
        assert isinstance(another, Term) or another == ''
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
        assert isinstance(term, Term)
        self.adopt_term(term)
        self.adopt_extail(extail)

    def adopt_term(self, term):
        self.term = term
        term.parent = self
        return self

    def adopt_extail(self, extail):
        self.extail = extail
        extail.parent = self
        return self

    def copy(self, expr):
        assert isinstance(expr, ExprCommon)
        self.adopt_term(expr.term)
        self.adopt_extail(expr.extail)
        return self

    def add_extail(self, tail):
        if isinstance(tail, Empty):
            return None
        traveler = self
        while isinstance(traveler.extail, ExTail):
            traveler = traveler.extail
        traveler.adopt_extail(tail)
        return self

    # def child_simplify(self): # later
    #     self.extail.child_simplify()
    #     self.term.simplify()
    #     return self

    def child_simplify(self): #temporary
        self.extail.child_simplify()
        self.simplify_term()
        return self

    def simplify_term(self):
        before = 'before'
        after = str(self.term)
        while before != after:
            self.term.simplify()
            before = after
            after = str(self.term)

    def unparenize(self):
        self.extail.unparenize()
        if isinstance(self.term.termtail, Empty) and\
           isinstance(self.term.factor, Paren):
            expr = self.term.factor.base
            expr *= self.term.coeff
            expr.add_extail(self.extail)
            self.copy(expr)
        return self

    def sort(self): # n square complexity
        self.extail.sort()
        traveler = self
        while isinstance(traveler.extail, ExTail) and self.term < traveler.extail.term:
            traveler = traveler.extail
        traveler.adopt_extail(ExTail('+', self.term, traveler.extail))
        self.copy(self.extail)
        return self

#############temp###################
    def monic(self, div_factor=1.):
        if isinstance(self, Expr):
            new = deepcopy(self)
            div_factor = self.term.coeff
        else:
            new = self
        new.term.coeff /= div_factor
        if isinstance(new.extail, ExTail):
            new.extail = new.extail.monic(div_factor)
        return new
###############temp end#############

    def __repr__(self):
        return str(self)


    def __eq__(self, another):
        if is_num(another):
            another_str = str(MetaExpr(Expr(Term(Num(another)))))
        else:
            another_str = str(another)
        return str(self) == another_str

    def __neg__(self):
        new = deepcopy(self)
        new.term = -new.term
        if isinstance(new.extail, ExTail):
            new.extail = -new.extail
        return new

    def __mul__(self, another):
        assert isinstance(another, Factor) or\
            isinstance(another, TermCommon) or\
            isinstance(another, Expr) or\
            isinstance(another, float) or\
            isinstance(another, int)
        
        if isinstance(self, Expr):
            new = deepcopy(self)
        else:
            new = self
        another = deepcopy(another)

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
#        self.simplify()

    def simplify(self):
        self.child_simplify()
        self.unparenize()
        self.sort()
        self.gather()
        self.remove_zeros()
        return self

    def gather(self):
        self.extail.gather()
        return self

    def remove_zeros(self):
        self.extail.remove_zeros()
        # if self.term.coeff == 0:
        #     self.copy(self.extail)
        return self

    def tailized(self):
        return ExTail('+', self.term, self.extail)

###### temporary start ###########
    def is_single_factor(self, instance):
        extail_check = isinstance(self.extail, Empty)
        termtail_check = isinstance(self.term.termtail, Empty)
        if instance != 0:
            factor_check = isinstance(self.term.factor, instance)
        else:
            factor_check = isinstance(self.term.factor)
        return extail_check and termtail_check and factor_check

    def simplified(self):
        self.simplify()
        return self

    def penetrate(self):
        self.term.factor.penetrate()
        return self

######### end ############

    def __str__(self):
        op_str = ''
        term_str = str(self.term)
        extail_str = str(self.extail)
        coeff = self.term.coeff
        coeff_str = str(coeff)+'*'
        if coeff == 1:
            coeff_str = ''
        elif coeff == -1:
            coeff_str = '-'
        elif isinstance(self.term.factor, Num):
            coeff_str = str(coeff)
            term_str = str(self.term.termtail)
        return '%s%s%s'%(coeff_str, term_str, extail_str)

    def __add__(self, another):
        assert isinstance(another, Expr)
        expr = deepcopy(self)
        another = deepcopy(another)
        expr.add_extail(another.tailized())
        expr.simplify()
        return expr

class ExTail(ExprCommon):
    def __init__(self, op, term, extail=Empty()):
        ExprCommon.__init__(self, term, extail)
        self.op = op
        self.remove_minus_op()

    def gather(self):
        self.extail.gather()
        if self.term == self.parent.term:
            self.parent.term.coeff += self.term.coeff
            self.parent.adopt_extail(self.extail)

    def remove_zeros(self):
        self.extail.remove_zeros()
        if self.term.coeff == 0:
            self.parent.adopt_extail(self.extail)

    def remove_minus_op(self):
        if self.op == '-':
            self.op = '+'
            self.term *= -1

##########temp###########
    def simplify(self):
        pass
###############end#########

    def __str__(self):
        op_str = self.op
        term_str = str(self.term)
        extail_str = str(self.extail)
        coeff = self.term.coeff
        coeff_str = str(coeff)+'*'
        if coeff == 1:
            coeff_str = ''
        elif coeff == -1:
            coeff_str = '-'
        elif isinstance(self.term.factor, Num):
            coeff_str = str(coeff)
            term_str = str(self.term.termtail)
        return '%s%s%s%s'%(op_str, coeff_str, term_str, extail_str)


class MetaExpr:
    def __init__(self, given):
        self.expr = given
        self.expr.simplify()

    def __eq__(self, another):
        return self.expr == another

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.expr)
