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

reserved = ['if', 'define', 'quote', 'lambda', 'eq', '>', '>=', '<', '<=', '+', '-', 'mod', '/', '*']


def evaluate(ast, env):
    """Evaluate an Abstract Syntax Tree in the specified environment."""
    if is_boolean(ast):
        return ast
    elif is_integer(ast):
        return ast
    elif is_symbol(ast):
        return env.lookup(ast)

    if is_list(ast) and len(ast) > 0:
        if is_closure(ast[0]):
            expected = len(ast[0].params)
            given = len(ast[1:])
            if given != expected:
                raise DiyLangError(f'wrong number of arguments, expected {expected} got {given}')
            p = {}
            for i in range(expected):
                p[ast[0].params[i]] = evaluate(ast[i+1], env)
            l_env = ast[0].env.extend(p)
            return evaluate(ast[0].body, l_env)

        if ast[0] == 'quote':
            return ast[1]
        elif ast[0] == 'atom':
            rest = evaluate(ast[1], env)
            return is_atom(rest)

        if ast[0] == 'eq':
            sample = evaluate(ast[1], env)
            if not is_atom(sample):
                return False
            for o in ast[2:]:
                if sample != evaluate(o, env):
                    return False
            return True

        elif ast[0] == '+':
            res = 0
            for i in ast[1:]:
                ei = evaluate(i, env)
                if not is_integer(ei):
                    raise DiyLangError('{} is not an integer'.format(ei))
                res += ei
            return res

        elif ast[0] == '-':
            res = evaluate(ast[1], env)
            if not is_integer(res):
                raise DiyLangError('{} is not an integer'.format(res))
            for i in ast[2:]:
                ei = evaluate(i, env)
                if not is_integer(ei):
                    raise DiyLangError('{} is not an integer'.format(ei))
                res -= ei
            return res

        elif ast[0] == '*':
            res = 1
            for i in ast[1:]:
                ei = evaluate(i, env)
                if not is_integer(ei):
                    raise DiyLangError('{} is not an integer'.format(ei))
                res *= ei
            return res

        elif ast[0] == '/':
            res = evaluate(ast[1], env)
            if not is_integer(res):
                raise DiyLangError(f'{res} is not an integer')
            for i in ast[2:]:
                ei = evaluate(i, env)
                if not is_integer(ei):
                    raise DiyLangError(f'"{ei}" is not an integer')
                res //= ei
            return res

        elif ast[0] == 'mod':
            res = evaluate(ast[1], env)
            if not is_integer(res):
                raise DiyLangError(f'"{res}" is not an integer')
            for i in ast[2:]:
                ei = evaluate(i, env)
                if not is_integer(ei):
                    raise DiyLangError(f'"{res}" is not an integer')
                res %= ei
            return res

        elif ast[0] == '>':
            sample = evaluate(ast[1], env)
            for i in ast[2:]:
                r = evaluate(i, env)
                if r >= sample:
                    return False
                sample = r
            return True

        elif ast[0] == '<':
            sample = evaluate(ast[1], env)
            for i in ast[2:]:
                r = evaluate(i, env)
                if r <= sample:
                    return False
                sample = r
            return True

        elif ast[0] == '>=':
            sample = evaluate(ast[1], env)
            for i in ast[2:]:
                r = evaluate(i, env)
                if r > sample:
                    return False
                sample = r
            return True

        elif ast[0] == '<=':
            sample = evaluate(ast[1], env)
            for i in ast[2:]:
                r = evaluate(i, env)
                if r < sample:
                    return False
                sample = r
            return True

        elif ast[0] == 'if':
            if len(ast) != 4:
                raise DiyLangError('IF expects condition and 2 branches')
            res = evaluate(ast[1], env)
            if not is_boolean(res):
                raise DiyLangError('IF condition must be boolean')
            if res:
                return evaluate(ast[2], env)
            else:
                return evaluate(ast[3], env)

        elif ast[0] == 'define':
            if len(ast) != 3:
                raise DiyLangError('Wrong number of arguments')
            if not is_symbol(ast[1]):
                raise DiyLangError(f'"{ast[1]}" is not a symbol')
            env.set(ast[1], evaluate(ast[2], env))
            return

        elif ast[0] == 'lambda':
            if len(ast) > 3:
                raise DiyLangError('Wrong number of arguments')
            if len(ast) == 1:
                params = []
                body = ast[1]
            else:
                params = ast[1]
                body = ast[2]
            if not is_list(params):
                raise DiyLangError('Params must be a list')
            return Closure(env, params, body)

        elif ast[0] == 'cons':


        elif is_symbol(ast[0]) or is_list(ast[0]):
            fn = evaluate(ast[0], env)
            return evaluate([fn]+ast[1:], env)
        else:
            raise DiyLangError(f'{ast[0]} not a function')
    else:
        if len(ast) > 0:
            raise DiyLangError(f'{ast[0]} is not defined')
        else:
            raise DiyLangError(f'empty expression')

