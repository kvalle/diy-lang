# -*- coding: utf-8 -*-

import re
from ast import is_boolean, is_list, is_atom
from types import LispError

"""
This is the parser module, with the `parse` function which you'll implement as part 1 of
the workshop. Its job is to convert strings into data structures that the evaluator can 
understand. 
"""

def parse(source):
    """Parse string representation of one *single* expression
    into the corresponding Abstract Syntax Tree."""

    source = remove_comments(source)

    ast = parse_expressions(source)

    if len(ast) == 1:
	return ast[0]

    return ast

def parse_expressions(source):
    expressions = split_exps(source)

    ast = []
    for expression in expressions:
        if expression[0] != '(':
            ast.append(parse_atom(expression))
        else:
            ast.append(parse_list(expression))

    return ast

def parse_atom(atom):
    if atom == "#t":
        return True
    elif atom == "#f":
        return False
    elif atom.isdigit():
        return int(atom)
    elif atom[0] == "'":
        return parse_quote_shorthand(atom)
    else:
        return atom

def parse_list(expression):
    expression = expression[1:-1];
    return parse_expressions(expression)

def parse_quote_shorthand(expression):
    if expression[0] != "'":
        if expression[0] != '(':
            return parse_atom(expression)
        else:
            return parse_list(expression)

    ast = []
    ast.append("quote")
    ast.append(parse_quote_shorthand(expression[1:]))

    return ast

##
## Below are a few useful utility functions. These should come in handy when 
## implementing `parse`. We don't want to spend the day implementing parenthesis 
## counting, after all.
## 

def remove_comments(source):
    """Remove from a string anything in between a ; and a linebreak"""
    return re.sub(r";+.*\n", "\n", source)

def find_matching_paren(source, start=0):
    """Given a string and the index of an opening parenthesis, determines 
    the index of the matching closing paren."""

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
    that can be parsed individually.

    Example: 
        > split_exps("foo bar (baz 123)")
        ["foo", "bar", "(baz 123)"]
    """

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
    elif source[0] == ")":
        raise LispError("Expected EOF")
    else:
        match = re.match(r"^[^\s)']+", source)
        end = match.end()
        atom = source[:end]
        return atom, source[end:]

##
## The functions below, `parse_multiple` and `unparse` are implemented in order for
## the REPL to work. Don't worry about them when implementing the language.
##

def parse_multiple(source):
    """Creates a list of ASTs from program source constituting multiple expressions.

    Example:

        >>> parse_multiple("(foo bar) (baz 1 2 3)")
        [['foo', 'bar'], ['baz', 1, 2, 3]]

    """

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
