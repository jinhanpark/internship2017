from nodes import *
from my_tokenizer import *

def get_expr(tokens):
    term = get_term(tokens)
    extail = get_extail(tokens)
    return Expr(term, extail)

def get_extail(tokens):
    if tokens.have_elt() and is_add_op(tokens.this()):
        op = tokens.get('add_op')
        expr = get_expr(tokens)
        return ExTail(op, expr)
    else:
        return Empty()

def get_term(tokens):
    factor = get_factor(tokens)
    termtail = get_termtail(tokens)
    return Term(factor, termtail)

def get_termtail(tokens):
    if tokens.have_elt() and is_mul_op(tokens.this()):
        op = tokens.get('mul_op')
        term = get_term(tokens)
        return TermTail(op, term)
    else:
        return Empty()

def get_factor(tokens):
    this = tokens.this()
    coeff = 1
    while this == '-':
        coeff *= -1
        tokens.get('add_op')
        this = tokens.this()
    if is_oparen(this):
        factor = get_paren(tokens, coeff)
    elif is_func_name(this):
        factor = get_func(tokens, coeff)
    else:
        factor = get_atom(tokens, coeff)
    return factor

def get_paren(tokens, coeff = 1):
    tokens.get('oparen')
    expr = get_expr(tokens)
    end = tokens.get('cparen')
    if end == ')':
        return Paren(expr, coeff)
    else:
        raise SyntaxError("No expected ')'")

def get_func(tokens, coeff = 1):
    name = tokens.get('func')
    expr = get_expr(tokens)
    if name == 'pow(':
        base = expr
        tokens.get('comma')
        ind = get_expr(tokens)
        tokens.get('cparen')
        return Pow(base, ind, coeff)
    tokens.get('cparen')
    if name == 'sin(':
        return Sin(expr, coeff)
    elif name == 'cos(':
        return Cos(expr, coeff)
    elif name == 'tan(':
        return Tan(expr, coeff)
    elif name == 'arcsin(':
        return ArcSin(expr, coeff)
    elif name == 'arccos(':
        return ArcCos(expr, coeff)
    elif name == 'arctan(':
        return ArcTan(expr, coeff)
    elif name == 'log(':
        return Log(expr, coeff)
    else:
        print "It shoudn't happen"

def get_atom(tokens, coeff=1):
    this = tokens.this()
    if is_num(this):
        this = tokens.get('num')
        return Num(this, coeff)
    elif is_const(this):
        this = tokens.get('const')
        return Const(this, coeff)
    elif is_var(this):
        this = tokens.get('var')
        return Var(this, coeff)
    else:
        raise SyntaxError("Unexpected token %s" % this)
