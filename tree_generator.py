from nodes import *
from my_tokenizer import *

def get_expr(tokens):
    term = get_term(tokens)
    extail = get_extail(tokens)
    return Expr(term, extail)

def get_extail(tokens):
    if tokens.have_elt():
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
    if tokens.have_elt():
        op = tokens.get('mul_op')
        term = get_term(tokens)
        return TermTail(op, term)
    else:
        return Empty()

def get_factor(tokens):
    if is_oparen(tokens.values[0]):
        factor = get_paren(tokens)
    else:
        factor = get_atom(tokens)
    return factor

def get_paren(tokens):
    tokens.get('oparen')
    expr = get_expr(tokens)
    end = tokens.get('cparen')
    if end == ')':
        return Paren(expr)
    else:
        raise SyntaxError("No expected ')'")

def get_atom(tokens):
    today = tokens.values[0]
    if today == '-':
        tomorrow = tokens.values[1]
    else:
        tomorrow = today
        today = ''
    this = today + tomorrow
    if is_num(this):
        return Num(this)
    elif is_const(this):
        return Const(tokens)
    elif is_variable(this):
        return Var(tokens)
    elif is_func_name(this):
        return Func(tokens)
    else:
        raise SyntaxError("Unexpected token %s" % this)

## Num, Const, Var, Func inherits from Atom
