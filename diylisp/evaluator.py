# -*- coding: utf-8 -*-

from types import Environment, LispError, Closure
from ast import is_boolean, is_atom, is_symbol, is_list, is_closure, is_integer
from asserts import assert_exp_length, assert_valid_definition, assert_boolean
from parser import unparse

"""
This is the Evaluator module. The `evaluate` function below is the heart
of your language, and the focus for most of parts 2 through 6.

A score of useful functions is provided for you, as per the above imports, 
making your work a bit easier. (We're supposed to get through this thing 
in a day, after all.)
"""

def evaluate(ast, env):
    """Evaluate an Abstract Syntax Tree in the specified environment."""

    if is_atom(ast):
        if is_symbol(ast):
            return env.lookup(ast)
        else:
            return ast
    elif ast[0] == "quote":
        if len(ast) != 2:
            raise LispError("quote takes one argument: %s" & unparse(ast))
        else:
            return evaluate(ast[1], env);
    elif ast[0] == "atom":
        if len(ast) != 2:
            raise LispError("atom takes one argument: %s" % unparse(ast))
        else:
            return is_atom(evaluate(ast[1], env))
    elif ast[0] == "eq":
        if len(ast) != 3:
            raise LispError("eq takes two arguments: %s" % unparse(ast))
        else:
	    arg1_evaluated = evaluate(ast[1], env)
	    arg2_evaluated = evaluate(ast[2], env)
	    
	    if not is_atom(arg1_evaluated) or not is_atom(arg2_evaluated):
                return False
            else:
                return arg1_evaluated == arg2_evaluated
    elif ast[0] == "+":
        if len(ast) != 3:
            raise LispError("+ takes two arguments: %s" % unparse(ast))
        else:
	    arg1_evaluated = evaluate(ast[1], env)
	    arg2_evaluated = evaluate(ast[2], env)

            if not is_integer(arg1_evaluated) or not is_integer(arg2_evaluated):
                raise LispError("arguments for + must be integers: %s" % unparse(ast))
            else:
                return arg1_evaluated + arg2_evaluated
    elif ast[0] == "-":
        if len(ast) != 3:
            raise LispError("- takes two arguments: %s" % unparse(ast))
        else:
	    arg1_evaluated = evaluate(ast[1], env)
	    arg2_evaluated = evaluate(ast[2], env)

            if not is_integer(arg1_evaluated) or not is_integer(arg2_evaluated):
                raise LispError("arguments for - must be integers: %s" % unparse(ast))
            else:
                return arg1_evaluated - arg2_evaluated
    elif ast[0] == "/":
        if len(ast) != 3:
            raise LispError("/ takes two arguments: %s" % unparse(ast))
        else:
	    arg1_evaluated = evaluate(ast[1], env)
	    arg2_evaluated = evaluate(ast[2], env)

            if not is_integer(arg1_evaluated) or not is_integer(arg2_evaluated):
                raise LispError("arguments for / must be integers: %s" % unparse(ast))
            else:
                return int(arg1_evaluated / arg2_evaluated)
    elif ast[0] == "*":
        if len(ast) != 3:
            raise LispError("* takes two arguments: %s" % unparse(ast))
        else:
	    arg1_evaluated = evaluate(ast[1], env)
	    arg2_evaluated = evaluate(ast[2], env)

            if not is_integer(arg1_evaluated) or not is_integer(arg2_evaluated):
                raise LispError("arguments for * must be integers: %s" % unparse(ast))
            else:
                return arg1_evaluated * arg2_evaluated
    elif ast[0] == ">":
        if len(ast) != 3:
            raise LispError("> takes two arguments: %s" % unparse(ast))
        else:
	    arg1_evaluated = evaluate(ast[1], env)
	    arg2_evaluated = evaluate(ast[2], env)

            if not is_integer(arg1_evaluated) or not is_integer(arg2_evaluated):
                raise LispError("arguments for > must be integers: %s" % unparse(ast))
            else:
                return arg1_evaluated > arg2_evaluated
    elif ast[0] == "mod":
        if len(ast) != 3:
            raise LispError("mod takes two arguments: %s" % unparse(ast))
        else:
	    arg1_evaluated = evaluate(ast[1], env)
	    arg2_evaluated = evaluate(ast[2], env)

            if not is_integer(arg1_evaluated) or not is_integer(arg2_evaluated):
                raise LispError("arguments for mod must be integers: %s" % unparse(ast))
            else:
                return arg1_evaluated % arg2_evaluated
    elif ast[0] == "if":
        if len(ast) != 4:
            raise LispError("if takes three arguments: %s" % unparse(ast))
        else:
            if evaluate(ast[1], env):
                return evaluate(ast[2], env)
            else:
                return evaluate(ast[3], env)
    elif ast[0] == "define":
        if len(ast) != 3:
            raise LispError("define takes two arguments: %s" % unparse(ast))
        else:
            if not is_symbol(ast[1]):
                raise LispError("the first argument for define must be a symbol: %s" % unparse(ast))
            else:
                env.set(ast[1], evaluate(ast[2], env))
                return ast[2]
    else:
        return ast
