# -*- coding: utf-8 -*-

from nose.tools import assert_equals

from diylisp.types import Environment
from diylisp.evaluator import evaluate
from diylisp.parser import parse

def test_nested_expression():
    """Remember, functions should evaluate their arguments. 

    (Except `quote` and `if`, that is, which aren't really functions...) Thus, 
    nested expressions should work just fine without any further work at this 
    point.

    If this test is failing, make sure that `+`, `>` and so on is evaluating 
    their arguments before operating on them."""

    ast = parse("(eq #f (> (- (+ 1 3) (* 2 (mod 7 4))) 4))")
    assert_equals(True, evaluate(ast, Environment()))


def test_basic_if_statement():
    """If statements are the basic control structures.

    The `if` should first evaluate its first argument. If this evaluates to true, then
    the second argument is evaluated and returned. Otherwise the third and last argument
    is evaluated and returned instead."""

    assert_equals(42, evaluate(parse("(if #t 42 1000)"), Environment()))
    assert_equals(1000, evaluate(parse("(if #f 42 1000)"), Environment()))
    assert_equals(True, evaluate(parse("(if #t #t #f)"), Environment()))


def test_that_only_correct_branch_is_evaluated():
    """The branch of the if statement that is discarded should never be evaluated."""

    ast = parse("(if #f (this should not be evaluated) 42)")
    assert_equals(42, evaluate(ast, Environment()))

def test_if_with_sub_expressions():
    """A final test with a more complex if expression.
    This test should already be passing if the above ones are."""

    ast = parse("""
        (if (> 1 2)
            (- 1000 1)
            (+ 40 (- 3 1)))
    """)
    assert_equals(42, evaluate(ast, Environment()))

def test_that_quote_does_not_evaluate_its_argument():
    """Calling `quote`, should still return its argument without evaluating it.
    This test should already be passing, but lets just make sure that `quote` still works
    as intended now that we have a few more powerful features."""

    ast = parse("""
        '(if (> 1 50)
             (- 1000 1)
             #f)
    """)
    assert_equals(['if', ['>', 1, 50], ['-', 1000, 1], False], evaluate(ast, Environment()))
