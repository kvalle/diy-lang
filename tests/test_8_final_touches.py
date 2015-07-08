# -*- coding: utf-8 -*-

from nose.tools import assert_equals
from nose.plugins.skip import SkipTest
from os.path import dirname, relpath, join

from diylisp.interpreter import interpret, interpret_file
from diylisp.types import Environment

env = Environment()
path = join(dirname(relpath(__file__)), '..', 'stdlib.diy')
interpret_file(path, env)

"""
In this last part, we provide tests for some suggestions on how to improve
the language a bit. Treat these tasks as optional, and suggestions only.
Feel free to do something completely different, if you fancy.
"""

"""
Suggestion 1: `cond`

First off, we will implement a new control structure found in most Lisps, the 
`cond` form (not to be confused with `cons`). The name `cond` is short for 
"conditional", and is sort of an buffed up version of `if`.

Implement this as a new case in the `evaluate` function in `evaluator.py`.
"""


def test_cond_returns_right_branch():
    """
    `cond` takes as arguments an variable a list of tuples (two-element lists, 
    or "conses").

    The first element of each tuple is evaluated in order, until noe evaluates 
    to `#t`. The second element of that tuple is returned. 
    """

    program = """
    (cond ((#f 'foo)
           (#t 'bar)
           (#f 'baz)))
    """
    assert_equals("bar", interpret(program, env))

def test_cond_dosnt_evaluate_all_branches():
    """
    Of all the second tuple elements, only the one we return is ever evaluated.
    """

    interpret("(define foo 42)", env)

    program = """
    (cond ((#f fire-the-missiles)
           (#t foo)
           (#f something-else-we-wont-do)))
    """
    assert_equals("42", interpret(program, env))

def test_cond_not_evaluating_more_predicateds_than_neccessary():
    """
    Once we find an predicate that evaluates to `#t`, no more predicates should
    be evaluated.
    """

    program = """
    (cond ((#f 1)
           (#t 2)
           (dont-evaluate-me! 3)))
    """
    assert_equals("2", interpret(program, env))

def test_cond_evaluates_predicates():
    """
    Remember to evaluate the predicates before checking whether they are true.
    """

    program = """
    (cond (((not #t) 'totally-not-true)
           ((> 4 3) 'tru-dat)))
    """

    assert_equals("tru-dat", interpret(program, env))

def test_cond_returnes_false_as_default():
    """
    If we evalaute all the predicates, only to find that none of them turned out 
    to be true, then `cond` should return `#f`.
    """

    program = """
    (cond ((#f 'no)
           (#f 'nope)
           (#f 'i-dont-even)))
    """

    assert_equals("#f", interpret(program, env))


"""
Suggestion 2: Strings
"""

"""
Suggestion 3: `let`
"""

"""
Suggestion 4: `defn`
"""

"""
Suggestion 5: IO
"""
