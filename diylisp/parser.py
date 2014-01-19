# -*- coding: utf-8 -*-

import re
from types import is_boolean, is_list
from types import LispError

def parse(source):
    """Parse string representation of one single expression
    into the corresponding Abstract Syntax Tree"""

    source = remove_comments(source)
    exp, rest = first_expression(source)
    if rest:
        raise LispError('Expected EOF')
    
    if exp == "#f":
        return False
    elif exp == "#t":
        return True
    elif exp.isdigit():
        return int(exp)
    elif exp[0] == "'":
        return ["quote", parse(exp[1:])]
    elif exp[0] == "(":
        end = find_matching_paren(exp)
        return [parse(e) for e in split_exps(exp[1:end])]
    else:
        return source

def parse_multiple(source):
    """Creates a list of ASTs from program source constituting multiple expressions"""

    source = remove_comments(source)
    return [parse(exp) for exp in split_exps(source)]

def unparse(ast):
    """Turns an AST back into lisp program source"""

    if is_boolean(ast):
        return "#t" if ast else "#f"
    elif is_list(ast):
        if len(ast) > 0 and ast[0] == "quote":
            return "'%s" % unparse(ast[1])
        else:
            return "(%s)" % " ".join([unparse(x) for x in ast])
    else:
        # integers or symbols (or lambdas)
        return str(ast)

def remove_comments(source):
    """Remove from a string anything in between a ; and a linebreak"""
    return re.sub(r";.*\n", "\n", source)

##
## Useful utility functions
## 

def find_matching_paren(source, start=0):
    """Given a string and the index of an opening parenthesis, determines 
    the index of the matching closing paren"""

    assert source[start] == '('
    pos = start
    open_brackets = 1
    while open_brackets > 0:
        pos += 1
        if len(source) == pos:
            raise LispError("Incomplete expression: %s" % source[start:])
        if source[pos] == '(':
            open_brackets += 1
        if source[pos] == ')':
            open_brackets -= 1
    return pos

def split_exps(source):
    """Splits a source string into subexpressions 
    that can be parsed individually"""

    rest = source.strip()
    exps = []
    while rest:
        exp, rest = first_expression(rest)
        exps.append(exp)
    return exps

def first_expression(source):
    """Split string into (exp, rest) where exp is the 
    first expression in the string and rest is the 
    rest of the string after this expression."""
    
    source = source.strip()
    if source[0] == "'":
        exp, rest = first_expression(source[1:])
        return source[0] + exp, rest
    elif source[0] == "(":
        last = find_matching_paren(source)
        return source[:last + 1], source[last + 1:]
    else:
        match = re.match(r"^[^\s)']+", source)
        end = match.end()
        atom = source[:end]
        return atom, source[end:]
