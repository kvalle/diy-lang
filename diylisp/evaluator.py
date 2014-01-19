# -*- coding: utf-8 -*-

from types import Environment
from types import LispError
from types import Lambda
from types import is_boolean, is_atom, is_symbol, is_list, is_lambda
from asserts import assert_exp_length, assert_valid_definition, assert_boolean
from parser import unparse

def evaluate(ast, env):
    """Evaluate an Abstract Syntax Tree in the specified environment."""
    if is_symbol(ast): return env.lookup(ast)
    elif is_atom(ast): return ast
    elif is_list(ast):
        if ast[0] == 'quote': return eval_quote(ast, env)
        elif ast[0] == 'atom': return eval_atom(ast, env)
        elif ast[0] == 'eq': return eval_eq(ast, env)
        elif ast[0] in ['+', '-', '*', '/', 'mod', '>']: 
            return eval_math(ast, env)

        elif ast[0] == 'if': return eval_if(ast, env)

        elif ast[0] == 'define': return eval_define(ast, env)        
        elif ast[0] == 'lambda': return eval_lambda(ast, env)

        elif ast[0] == 'cons': return eval_cons(ast, env)
        elif ast[0] == 'car': return eval_car(ast, env)
        elif ast[0] == 'cdr': return eval_cdr(ast, env)
        elif ast[0] == 'list': return eval_list(ast, env)

        elif is_lambda(ast[0]): return apply(ast, env)
        elif is_symbol(ast[0]) or is_list(ast[0]):
            fn = evaluate(ast[0], env)
            return evaluate([fn] + ast[1:], env)
        else:
            raise LispError("Call to: " + unparse(ast[0]))
    else:
        raise SyntaxError(ast)

def eval_quote(ast, env):
    assert_exp_length(ast, 2)
    return ast[1]

def eval_eq(ast, env):
    assert_exp_length(ast, 3)
    v1, v2 = evaluate(ast[1], env), evaluate(ast[2], env)
    return True if v1 == v2 and is_atom(v1) else False

def eval_math(ast, env):
    ops = {
        '+': lambda a, b: a + b,
        '-': lambda a, b: a - b,
        '*': lambda a, b: a * b,
        '/': lambda a, b: a / b,
        'mod': lambda a, b: a % b,
        '>': lambda a, b: a > b
    }
    op, a, b = ast
    return ops[op](evaluate(a, env), evaluate(b, env))

def eval_if(ast, env):
    assert_exp_length(ast, 4)
    _, pred, if_part, else_part = ast
    if evaluate(pred, env): 
        return evaluate(if_part, env) 
    else: 
        return evaluate(else_part, env)

def eval_atom(ast, env):
    arg = evaluate(ast[1], env)
    return is_atom(arg)

def eval_define(ast, env):
    assert_valid_definition(ast[1:])
    symbol = ast[1]
    value = evaluate(ast[2], env)
    env.set(symbol, value)
    return symbol

def eval_lambda(ast, env):
    assert_exp_length(ast, 3)
    (_, params, body) = ast
    return Lambda(params, body, env)

def apply(ast, env):
    fn = evaluate(ast[0], env)
    args = ast[1:]

    if len(args) != len(fn.params):
        msg = "Wrong number of arguments, expected %d got %d: %s" \
            % (len(fn.params), len(args), unparse(ast))
        raise LispError(msg)
    
    args = [evaluate(exp, env) for exp in ast[1:]]
    return evaluate(fn.body, env.extend(dict(zip(fn.params, args))))

def eval_cons(ast, env):
    car = evaluate(ast[1], env)
    cdr = evaluate(ast[2], env)
    return [car] if cdr == 'nil' else [car] + cdr

def eval_car(ast, env):
    lst = evaluate(ast[1], env)
    return lst[0]

def eval_cdr(ast, env):
    lst = evaluate(ast[1], env)
    return 'nil' if len(lst) == 0 else lst[1:]

def eval_list(ast, env):
    return map(lambda arg: evaluate(arg, env), ast[1:])
