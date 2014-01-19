# -*- coding: utf-8 -*-

from nose.tools import assert_equals

from diylisp.types import Environment
from diylisp.evaluator import evaluate
from diylisp.parser import parse

def test_nested_expression():
    """All functions (except `quote` wich isn't really a function) should evaluate the 
    arguments. Thus, nested expressions should work just fine without any further work 
    at this point."""

    nested_expression = parse("(> (- (+ 1 3) (* 2 (mod 7 4))) 4)")
    assert_equals(False, evaluate(nested_expression, Environment()))

def test_basic_if_statement():
    """If statements are the basic controll structures.

    The `if` should first evaluate it's first argument. If this evaluates to true, then
    the second argument is evaluated and returned. Otherwise the third and last argument
    is evaluated and returned instead."""

    if_expression = parse("(if #t 42 1000)")
    assert_equals(42, evaluate(if_expression, Environment()))

def test_that_only_correct_branch_is_evaluated():
    """The branch of the if statement that is discarded should never be evaluated."""

    if_expression = parse("(if #f (this should not be evaluated) 42)")
    assert_equals(42, evaluate(if_expression, Environment()))

def test_if_with_sub_expressions():
    """A final test with a more complex if expression.
    This test should already be passing if the above ones are."""

    if_expression = parse("""
        (if (> 1 2)
            (- 1000 1)
            (+ 40 (- 3 1)))
    """)
    assert_equals(42, evaluate(if_expression, Environment()))
