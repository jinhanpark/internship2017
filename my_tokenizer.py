import re

func_pattern = ["sin\(", 'cos\(', 'tan\(', 'arcsin\(', 'arccos\(', 'arctan\(', 'pow\(', 'log\(']
const_pattern = ["e", "pi"]
op_pattern = ['\+', '\*', '\-', '\/']
etc_pattern = ['\(|\)|\,']
num_pattern= ["0\.[0-9]*|\.[0-9]+|0|[1-9][0-9]*\.?[0-9]*"]

def tokenizer(expr):
    patterns = []

    global func_pattern
    global const_pattern
    global op_pattern
    global etc_pattern
    global num_pattern
    
    patterns.extend(func_pattern)
    patterns.extend(const_pattern)
    patterns.extend(op_pattern)
    patterns.extend(etc_pattern)
    patterns.extend(num_pattern)
    
    combined = '|'.join(patterns)
    pattern = '('+ combined + ')'
    expr = expr.replace(' ', '')
    tokens = re.split(pattern, expr)
    return [x for x in tokens if len(x)>0]

def token_type_list(token_list):
    type_list = []
    this = ''
    for token in token_list:
        if is_func_name(token):
            this = 'func'
        elif is_const(token):
            this = 'const'
        elif is_add_op(token):
            this = 'add_op'
        elif is_mul_op(token):
            this = 'mul_op'
        elif is_oparen(token):
            this = 'oparen'
        elif is_cparen(token):
            this = 'cparen'
        elif is_comma(token):
            this = 'comma'
        elif is_num(token):
            this = 'num'
        elif is_var(token):
            this = 'var'
        else:
            raise SyntaxError('Unexpected token type')
        type_list.append(this)
    return type_list

def is_func_name(token):
    global func_pattern
    pattern = '^'+ '$|^'.join(func_pattern) + '$'
    return re.match(pattern, token)

def is_const(token):
    global const_pattern
    return token in const_pattern

def is_add_op(token):
    lst = ['+', '-']
    return token in lst

def is_mul_op(token):
    lst = ['*', '/']
    return token in lst

def is_oparen(token):
    return token == '('

def is_cparen(token):
    return token == ')'

def is_comma(token):
    return token == ','

def is_num(token):
    global num_pattern
    pattern = '^' + num_pattern[0] + '$'
    return re.match(pattern, token)
    

def is_var(token):
    lst = ['x', 'y']
    return token in lst
    
class Tokens:
    def __init__(self, s):
        token_list = tokenizer(s)
        self.values = token_list
        self.type_list = token_type_list(token_list)

    def get(self, token_type):
        token = self.values.pop(0)
        true_type = self.type_list.pop(0)
        if token_type == true_type:
            return token
        else:
            raise TypeError("Unexpected '%s' token : %s"% (token_type, token))

    def insert(self, token, token_type):
        self.values.insert(0, token)
        self.type_list.insert(0, token_type)

    def have_elt(self):
        return len(self.values) > 0

    def this(self):
        return self.values[0]

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.values)
