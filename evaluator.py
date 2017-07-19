from nodes import *
from differentiator import diff_meta
from tree_generator import get_meta_expr
import re
import numpy as np

def is_continuous(meta, x='0'):
    return not np.isnan(eval_meta(meta, x))

def is_differentiable(meta, x='0'):
    return (not np.isnan(eval_meta(diff_meta(meta), x)) and\
            is_continuous(meta, x))

def replace_with(meta, x='None', y='None'):
    if y != 'None':
        assert x != 'None'
        x = '(%s)'%str(get_meta_expr(x))
        y = '(%s)'%str(get_meta_expr(y))
        expr_str = str(meta)
        expr_str = re.sub(r'y', 'save_for_y', expr_str)
        expr_str = re.sub(r'x', x, expr_str)
        expr_str = re.sub(r'save_for_y', y, expr_str)
        new = get_meta_expr(expr_str)
        return new
    if x != 'None':
        x = '(%s)'%str(get_meta_expr(x))
        expr_str = str(meta)
        expr_str = re.sub(r'x', x, expr_str)
        new = get_meta_expr(expr_str)
        return new
    else:
        return meta

def eval_meta(meta, x=None, y=None, with_pi=False):
    assert isinstance(meta, MetaExpr)
    try:
        x = '%f'%x
    except:
        x = str(x)
    try:
        y = '%f'%y
    except:
        y = str(y)
    try:
        if with_pi:
            x = x+'*pi'
            y = y+'*pi'
        new = replace_with(meta, x, y)
        result = eval_expr(new.expr, round_bound=5)
        return result
    except:
        return np.nan

def eval_expr(given, round_bound=10):
    assert isinstance(given, Expr)
    return round(eval_term(given.term) + eval_extail(given.extail), round_bound)

def eval_extail(given):
    if isinstance(given, ExTail):
        return eval_term(given.term) + eval_extail(given.extail)
    elif isinstance(given, Empty):
        return 0.
    else:
        raise ValueError

def eval_term(given):
    assert isinstance(given, Term)
    return given.coeff*eval_factor(given.factor) * eval_termtail(given.termtail)

def eval_termtail(given):
    if isinstance(given, TermTail):
        return eval_factor(given.factor) * eval_termtail(given.termtail)
    elif isinstance(given, Empty):
        return 1.
    else:
        raise ValueError

def eval_factor(given):
    assert isinstance(given, Factor)
    if isinstance(given, Literal):
        return eval_literal(given)
    elif isinstance(given, SinVarFunc):
        return eval_func(given)
    elif isinstance(given, Pow):
        return eval_pow(given)
    else:
        raise ValueError

def eval_literal(given):
    assert not isinstance(given, Var) # no variable
    if isinstance(given, Num):
        return 1.
    elif isinstance(given, Const):
        return eval_const(given)
    else:
        raise ValueError

def eval_const(given):
    const = str(given)
    if const == 'e':
        return math.exp(1)
    elif const == 'pi':
        return math.pi

def eval_func(given):
    assert given.exp == 1
    func = given.func_name
    base = eval_expr(given.base, round_bound=10)
    if func == '':
        result = base
    elif func == 'sin':
        result = math.sin(base)
    elif func == 'cos':
        result = math.cos(base)
    elif func == 'tan':
        result = math.tan(base)
    elif func == 'log':
        result = math.log(base)
    else:
        raise ValueError
    return round(result, 5)

def eval_pow(given):
    base = eval_expr(given.base)
    exp = eval_expr(given.exp)
    return round(math.pow(base, exp), 10)
