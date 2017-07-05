from nodes import *

def distribute(expr):
    pass

def dist_term(this_term):
    temp = this_term
    while temp.termtail.type != 'empty':
        if temp.factor.type == 'paren':
            temp.factor = right_dist(temp)
            temp.termtail = Empty()
            continue
        temp = temp.termtail.term
    if need_left_dist(this_term):
        this_term = calc_left_dist(this_term)
    return this_term

def right_dist(this_term):
    expr = this_term.factor.expr
    tail = this_term.termtail
    temp = expr
    while True:
        temp.term.add_tail(tail)
        if temp.extail.type == 'empty':
            break
        temp = temp.extail.expr
    return Paren(expr)



def left_dist(term):
    pass

def need_left_dist(term):
    return False
