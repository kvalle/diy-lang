# -*- coding: utf-8 -*-

from nose.tools import assert_equals, assert_raises_regexp

from diylisp.types import Environment
from diylisp.evaluator import evaluate
from diylisp.parser import parse

"""
We will start by implementing evaluation of simple expressions.
"""

def test_evaluating_boolean():
    """Booleans should evaluate to themselves."""
    assert_equals(True, evaluate(True, Environment()))
    assert_equals(False, evaluate(False, Environment()))

def test_evaluating_integer():
    """...and so should integers."""
    assert_equals(42, evaluate(42, Environment()))

def test_evaluating_quote():
    """When a call is done to the `quote` form, the argument should be returned without 
    being evaluated.

    (quote foo) -> foo
    """

    assert_equals("foo", evaluate(["quote", "foo"], Environment()))
    assert_equals([1, 2, False], evaluate(["quote", [1, 2, False]], Environment()))

def test_evaluating_atom_function():
    """The `atom` form is used to determine whether an expression is an atom.

    Atoms are expressions that are not list, i.e. integers, booleans or symbols.
    Remember that the argument to `atom` must be evaluated before the check is done.
    """

    assert_equals(True, evaluate(["atom", True], Environment()))
    assert_equals(True, evaluate(["atom", False], Environment()))
    assert_equals(True, evaluate(["atom", 42], Environment()))
    assert_equals(True, evaluate(["atom", ["quote", "foo"]], Environment()))
    assert_equals(False, evaluate(["atom", ["quote", [1, 2]]], Environment()))

def test_evaluating_eq_function():
    """"""

    assert_equals(True, evaluate(["eq", 1, 1], Environment()))
    assert_equals(False, evaluate(["eq", 1, 2], Environment()))

    # From this point, the ASTs might sometimes be too long or cummbersome to
    # write down explicitly, and we'll use `parse` to make them for us.
    # Remember, if you need to have a look at exactly what is passed to `evaluate`, 
    # just add a print statement.

    assert_equals(True, evaluate(parse("(eq 'foo 'foo)"), Environment()))
    assert_equals(False, evaluate(parse("(eq 'foo 'bar)"), Environment()))
    
    assert_equals(False, evaluate(parse("(eq '(1 2) '(1 2))"), Environment()))


def test_basic_math_operators():
    """To be able to do anything useful, we need some basic math operators.

    Since we only operate with integers, `/` must represent integer division.
    `mod` is the modulo operator.
    """

    assert_equals(4, evaluate(["+", 2, 2], Environment()))
    assert_equals(1, evaluate(["-", 2, 1], Environment()))
    assert_equals(3, evaluate(["/", 6, 2], Environment()))
    assert_equals(3, evaluate(["/", 7, 2], Environment()))
    assert_equals(6, evaluate(["*", 2, 3], Environment()))
    assert_equals(1, evaluate(["mod", 7, 2], Environment()))
    assert_equals(True, evaluate([">", 7, 2], Environment()))
    assert_equals(False, evaluate([">", 2, 7], Environment()))
    assert_equals(False, evaluate([">", 7, 7], Environment()))
