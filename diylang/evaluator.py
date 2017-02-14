# -*- coding: utf-8 -*-

from .types import Environment, DiyLangError, Closure, String
from .ast import is_boolean, is_atom, is_symbol, is_list, is_closure, \
    is_integer, is_string
from .parser import unparse

"""
This is the Evaluator module. The `evaluate` function below is the heart
of your language, and the focus for most of parts 2 through 6.

A score of useful functions is provided for you, as per the above imports,
making your work a bit easier. (We're supposed to get through this thing
in a day, after all.)
"""


def evaluate(ast, env):
    """Evaluate an Abstract Syntax Tree in the specified environment."""

    if is_boolean(ast):
        return ast
    elif is_integer(ast):
        return ast
    elif is_string(ast):
        return ast
    elif is_list(ast):
        if ast == []:
            raise DiyLangError("Cannot evaluate empty list")
        elif is_form(ast, 'quote'):
            return ast[1]
        elif is_form(ast, 'atom'):
            return evaluate_atom(ast, env)
        elif is_form(ast, 'eq'):
            return evaluate_eq(ast, env)
        elif is_math(ast):
            return evaluate_math(ast, env)
        elif is_form(ast, 'if'):
            return evaluate_if(ast, env)
        elif is_form(ast, 'cond'):
            return evaluate_cond(ast, env)
        elif is_form(ast, 'cons'):
            return evaluate_cons(ast, env)
        elif is_form(ast, 'head'):
            return evaluate_head(ast, env)
        elif is_form(ast, 'tail'):
            return evaluate_tail(ast, env)
        elif is_form(ast, 'empty'):
            return evaluate_empty(ast, env)
        elif is_form(ast, 'let'):
            return evaluate_let(ast, env)
        elif is_form(ast, 'define'):
            return evaluate_define(ast, env)
        elif is_form(ast, 'defn'):
            return evaluate_defn(ast, env)
        elif is_form(ast, 'lambda'):
            return evaluate_lambda(ast, env)
        elif is_closure(ast[0]):
            return evaluate_function_call(ast, env)
        elif is_symbol(ast[0]) or is_list(ast[0]):
            evaluated = evaluate(ast[0], env)
            return evaluate([evaluated] + ast[1:], env)
        else:
            raise DiyLangError("Tried to call {}, which is not a function".format(unparse(ast[0])))

    return env.lookup(ast)


math_operators = {
    '+' : lambda x, y: x + y,
    '-' : lambda x, y: x - y,
    '/' : lambda x, y: x / y,
    '*' : lambda x, y: x * y,
    'mod' : lambda x, y: x % y,
    '>' : lambda x, y: x > y
}

def is_form(ast, f):
    return ast[0] == f

def is_math(ast):
    return ast[0] in math_operators.keys()

def evaluate_atom(ast, env):
    return is_atom(evaluate(ast[1], env))

def evaluate_eq(ast, env):
    arg1 = evaluate(ast[1], env)
    arg2 = evaluate(ast[2], env)
    return arg1 == arg2 and is_atom(arg1)

def evaluate_math(ast, env):
    arg1 = evaluate(ast[1], env)
    arg2 = evaluate(ast[2], env)
    if is_integer(arg1) and is_integer(arg2):
        return math_operators[ast[0]](arg1, arg2)
    else:
        raise DiyLangError("Math operators can only be used on numbers")

def evaluate_if(ast, env):
    test = evaluate(ast[1], env)
    if test:
        return evaluate(ast[2], env)
    else:
        return evaluate(ast[3], env)

def evaluate_cond(ast, env):
    branches = ast[1]
    for branch in branches:
        if evaluate(branch[0], env):
            return evaluate(branch[1], env)

    return False

def evaluate_cons(ast, env):
    head = evaluate(ast[1], env)
    tail = evaluate(ast[2], env)
    if is_list(tail):
        return [head] + tail
    else:
        if is_string(head) and is_string(tail):
            return String(head.val + tail.val)
        else:
            raise DiyLangError("Cannot call cons on non-string or non-list")

def evaluate_head(ast, env):
    val = evaluate(ast[1], env)

    if is_string(val):
        if val == "":
            raise DiyLangError("Cannot call head on empty string")
        else:
            return String(val.val[0])
    elif is_list(val):
        if val == []:
            raise DiyLangError("Cannot call head on empty list")
        else:
            return val[0]


    raise DiyLangError("Cannot call head on non-list or non-string")


def evaluate_tail(ast, env):
    val = evaluate(ast[1], env)

    if is_string(val):
        if val == "":
            raise DiyLangError("Cannot call tail on empty string")
        else:
            return String(val.val[1:])
    elif is_list(val):
        if val == []:
            raise DiyLangError("Cannot call tail on empty list")
        else:
            return val[1:]


    raise DiyLangError("Cannot call tail on non-list or non-string")

def evaluate_empty(ast, env):
    val = evaluate(ast[1], env)

    if is_string(val):
        return val.val == ""
    elif is_list(val):
        return val == []

    raise DiyLangError("Cannot call empty on non-list")

def evaluate_let(ast, env):
    bindings, expression = ast[1], ast[2]
    for binding in bindings:
        name = binding[0]
        value = evaluate(binding[1], env)
        env = env.extend({name: value})

    return evaluate(expression, env)

def evaluate_define(ast, env):
    if len(ast) != 3:
        raise DiyLangError("Wrong number of arguments")

    symbol = ast[1]
    value = evaluate(ast[2], env)
    if not is_symbol(symbol):
        raise DiyLangError("{} is not a symbol".format(unparse(symbol)))

    env.set(symbol, value)
    return symbol

def evaluate_defn(ast, env):
    symbol = ast[1]
    closure = evaluate(['lambda', ast[2], ast[3]], env)
    env.set(symbol, closure)
    return symbol

def evaluate_lambda(ast, env):
    if not is_list(ast[1]):
        raise DiyLangError("The parameters of lambda should be a list")

    if len(ast) != 3:
        raise DiyLangError("Wrong number of arguments")

    return Closure(env, ast[1], ast[2])

def evaluate_function_call(ast, env):
    closure = ast[0]
    params = closure.params
    args = ast[1:]

    if len(params) != len(args):
        raise DiyLangError("wrong number of arguments, expected {} got {}".format(len(params), len(args)))

    evaluated_args = [evaluate(arg, env) for arg in args]
    new_env = closure.env.extend(dict(zip(params, evaluated_args)))
    return evaluate(closure.body, new_env)
