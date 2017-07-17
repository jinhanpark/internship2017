from nodes import *
from tree_generator import get_meta_expr
import re

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

def eval_meta(meta, x=None, y=None):
    assert isinstance(meta, MetaExpr)
    if is_num(x):
        x = '%f'%x
    else:
        x = str(x)
    if is_num(y):
        y = '%f'%y
    else:
        y = str(y)
    new = replace_with(meta, x, y)
    return round(eval_expr(new.expr), 10)

def eval_expr(given, x='0', y='0'):
    assert isinstance(given, Expr)
    return eval_term(given.term) + eval_extail(given.extail)

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
    base = eval_expr(given.base)
    if func == '':
        return base
    elif func == 'sin':
        return math.sin(base)
    elif func == 'cos':
        return math.cos(base)
    elif func == 'tan':
        return math.tan(base)
    elif func == 'log':
        return math.log(base)
    else:
        raise ValueError

def eval_pow(given):
    base = eval_expr(given.base)
    exp = eval_expr(given.exp)
    return math.pow(base, exp)
