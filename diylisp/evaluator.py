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
            return ast[1];
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
                return env.lookup(ast[1])
    elif ast[0] == "lambda":
        if len(ast) != 3:
            raise LispError("lamba takes two arguments: %s" % unparse(ast))
        else:
            if not is_list(ast[1]):
                raise LispError("the argument list for a lambda must be a list: %s" % unparse(ast))
            else:
                return Closure(env, ast[1], ast[2])
    elif is_closure(ast[0]):
        return evaluate_closure(ast, env)
    elif ast[0] == "cons":
        if len(ast) != 3:
            raise LispError("cons takes two arguments: %s" % unparse(ast))
        else:
            arg1_evaluated = evaluate(ast[1], env)
            arg2_evaluated = evaluate(ast[2], env)

            if not is_atom(arg1_evaluated):
                raise LispError("the first argument to cons must be an atom: %s" % unparse(ast))
            elif not is_list(arg2_evaluated):
                raise LispError("the second argument to cons must be a list: %s" % unparse(ast))
            else:
                new_list = []
                new_list.append(arg1_evaluated)
                new_list += arg2_evaluated
                return new_list
    elif ast[0] == "head":
        if len(ast) != 2:
            raise LispError("head takes one argument: %s" % unparse(ast))
        else:
            arg_evaluated = evaluate(ast[1], env)

            if not is_list(arg_evaluated):
                raise LispError("the argument to head must be a list: %s" % unparse(ast))
            elif len(arg_evaluated) < 1:
                raise LispError("the argument to head needs at least one element: %s" % unparse(ast))
            else:
                return arg_evaluated[0]
    elif ast[0] == "tail":
        if len(ast) != 2:
            raise LispError("tail takes one argument: %s" % unparse(ast))
        else:
            arg_evaluated = evaluate(ast[1], env)

            if not is_list(arg_evaluated):
                raise LispError("the argument to tail must be a list: %s" % unparse(ast))
            elif len(arg_evaluated) < 1:
                raise LispError("the argument to tail needs at least one element: %s" % unparse(ast))
            else:
                return arg_evaluated[1:]
    elif ast[0] == "empty":
        if len(ast) != 2:
            raise LispError("empty takes one argument: %s" % unparse(ast))
        else:
            arg_evaluated = evaluate(ast[1], env)

            if not is_list(arg_evaluated):
                raise LispError("the argument to empty must be a list: %s" % unparse(ast))
            elif len(arg_evaluated) < 1:
                return True
            else:
                return False
    else:
        closure = evaluate(ast[0], env)
        if not is_closure(closure):
            raise LispError("only closures can be called: %s" % unparse(ast))

        closure_eval_list = []
        closure_eval_list.append(closure)
        closure_eval_list += ast[1:]
        return evaluate_closure(closure_eval_list, env)

def evaluate_closure(ast, env):
    if len(ast[0].params) != len(ast) - 1:
        raise LispError("lambda called with the wrong number of arguments, expected %d, got %d: %s" % (len(ast[0].params), len(ast) - 1, unparse(ast)))

    closure_eval_env = ast[0].env.extend({})
    i = 0
    while i < len(ast[0].params):
        closure_eval_env.set(ast[0].params[i], evaluate(ast[i + 1], env))
        i += 1

    return evaluate(ast[0].body, closure_eval_env)
