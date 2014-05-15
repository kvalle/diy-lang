# -*- coding: utf-8 -*-

from os.path import dirname, join

from evaluator import evaluate
from parser import parse, unparse, parse_multiple
from types import Environment


def interpret(source, env=None):
    """
    Interpret a lisp program statement

    Accepts a program statement as a string, interprets it, and then
    returns the resulting lisp expression as string.
    """
    if env is None:
        env = Environment()

    return unparse(evaluate(parse(source), env))


def interpret_file(filename, env=None):
    """
    Interpret a lisp file

    Accepts the name of a lisp file containing a series of statements. 
    Returns the value of the last expression of the file.
    """
    if env is None:
        env = Environment()

    with open(filename, 'r') as sourcefile:
        source = "".join(sourcefile.readlines())

    asts = parse_multiple(source)
    results = [evaluate(ast, env) for ast in asts]
    return unparse(results[-1])
