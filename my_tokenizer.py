import re
import string

def tokenizer(expr):
    patterns = []
    
    func_pattern = ["sin\(", 'cos\(', 'tan\(', 'arc', 'pow\(', 'log\(']
    const_pattern = ["e", "pi"]
    op_pattern = ['\+', '\*', '\-', '\/']
    num_pattern= ["\(|\)|0\.[0-9]*|\.[0-9]+|0|[1-9][0-9]*\.?[0-9]*"]
    
    patterns.extend(func_pattern)
    patterns.extend(const_pattern)
    patterns.extend(op_pattern)
    patterns.extend(num_pattern)
    
    combined = string.join(patterns, '|')
    pattern = '('+ combined + ')'
    expr = expr.replace(' ', '')
    tokens = re.split(pattern, expr)
    return filter(None, tokens)
