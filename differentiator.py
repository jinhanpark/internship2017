from nodes import *


def diff_meta(given, scope='x'):
    assert isinstance(given, MetaExpr)
    new = MetaExpr(diff_expr(given.expr, scope))
    return new

def diff_expr(given, scope):
    assert isinstance(given, Expr)
    given = copy.deepcopy(given)
    new = Expr(diff_term(given.term, scope),
               diff_extail(given.extail, scope))
    return new

def diff_extail(given, scope):
    if isinstance(given, Empty):
        return given
    elif isinstance(given, ExTail):
        new = ExTail('*',
                     diff_term(given.term, scope),
                     diff_extail(given.extail, scope))
        return new
    else:
        raise ValueError

def diff_term(given, scope):
    assert isinstance(given, Term)
    left_term = Term(diff_factor(given.factor, scope),
                     given.termtail)
    if isinstance(given.termtail, Empty):
        result = left_term
    else:
        right_term = Term(given.factor,
                          diff_termtail(given.termtail, scope))
        total = Expr(left_term,
                     ExTail('+', right_term))
        new = Term(Paren(total))
        result = new
    result.coeff = given.coeff
    return result


def diff_termtail(given, scope):
    assert isinstance(given, TermTail)
    left_term = Term(diff_factor(given.factor, scope),
                     given.termtail)
    if isinstance(given.termtail, Empty):
        return left_term.tailized()
    else:
        right_term = Term(given.factor,
                          diff_termtail(given.termtail, scope))
        total = Expr(left_term,
                     ExTail('+', right_term))
        new = TermTail('*', Paren(total))
        return new

def diff_factor(given, scope):
    assert isinstance(given, Factor)
    if isinstance(given, Literal):
        return diff_literal(given, scope)
    elif isinstance(given, SinVarFunc):
        return diff_func(given, scope)
    elif isinstance(given, Pow):
        return diff_pow(given, scope)
    else:
        raise ValueError

def diff_literal(given, scope):
    if isinstance(given, Num) or\
       isinstance(given, Const):
        return Num(0.)
    elif isinstance(given, Var):
        if str(given) == scope:
            return Num(1.)
        elif str(given) == scope:
            return Num(1.)
        else:
            return Num(0.)

def diff_func(given, scope):
    assert given.exp == 1
    func = given.func_name
    chain_part = diff_expr(given.base, scope)

    if func == '':
        return Paren(chain_part)
    elif func == 'sin':
        func_part = Cos(given.base)
    elif func == 'cos':
        func_part = Sin(given.base, -1)
    elif func == 'log':
        func_part = Pow(given.base, num2expr(-1.))
    else:
        raise ValueError
    return Paren(Expr(Term(func_part,
                           TermTail('*', Paren(chain_part)))))

def diff_pow(given, scope):
    if scope in str(given.base) and\
       scope in str(given.exp):
        raise ValueError
    elif scope in str(given.base):
        exp_part = Paren(copy.deepcopy(given.exp))
        given.exp += num2expr(-1.)
        chain_part = Paren(diff_expr(given.base, scope))
        return Paren(Expr(Term(exp_part,
                               TermTail('*', given,
                                        TermTail('*', chain_part)))))
    elif scope in str(given.exp):
        log_part = Log(given.base)
        chain_part = Paren(diff_expr(given.exp, scope))
        return Paren(Expr(Term(log_part,
                               TermTail('*', given,
                                        TermTail('*', chain_part)))))
    else:
        return Num(0.)
