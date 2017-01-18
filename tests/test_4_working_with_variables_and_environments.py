# -*- coding: utf-8 -*-

from nose.tools import assert_equals, assert_raises_regexp

from diylang.types import DiyLangError, Environment
from diylang.evaluator import evaluate
from diylang.parser import parse

"""
Before we go on to evaluating programs using variables, we need to implement
an environment to store them in.

It is time to fill in the blanks in the `Environment` class located in `types.py`.
"""


def test_simple_lookup():
    """TEST 4.1: An environment should store variables and provide lookup.

    Tip: Implement this in the lookup() method in types.py.
    """

    env = Environment({"var": 42})
    assert_equals(42, env.lookup("var"))


def test_lookup_on_missing_raises_exception():
    """TEST 4.2: When looking up an undefined symbol, an error should be raised.

    The error message should contain the relevant symbol, and inform that it has
    not been defined.
    """

    with assert_raises_regexp(DiyLangError, "my-missing-var"):
        empty_env = Environment()
        empty_env.lookup("my-missing-var")


def test_lookup_from_inner_env():
    """TEST 4.3: The `extend` function returns a new environment extended with more bindings.

    Tip: The Dictionary class has a convenient .update method.
    """

    env = Environment({"foo": 42})
    env = env.extend({"bar": True})
    assert_equals(42, env.lookup("foo"))
    assert_equals(True, env.lookup("bar"))


def test_lookup_deeply_nested_var():
    """TEST 4.4: Extending overwrites old bindings to the same variable name."""

    env = Environment({"a": 1}).extend({"b": 2}).extend({"c": 3}).extend({"foo": 100})
    assert_equals(100, env.lookup("foo"))


def test_extend_returns_new_environment():
    """TEST 4.5: The extend method should create a new environment, leaving the old one unchanged."""

    env = Environment({"foo": 1})
    extended = env.extend({"foo": 2})

    assert_equals(1, env.lookup("foo"))
    assert_equals(2, extended.lookup("foo"))


def test_set_changes_environment_in_place():
    """TEST 4.6: When calling `set` the environment should be updated"""

    env = Environment()
    env.set("foo", 2)
    assert_equals(2, env.lookup("foo"))


def test_redefine_variables_illegal():
    """TEST 4.7: Variables can only be defined once.

    Setting a variable in an environment where it is already defined should result
    in an appropriate error.
    """

    env = Environment({"foo": 1})
    with assert_raises_regexp(DiyLangError, "already defined"):
        env.set("foo", 2)


"""
With the `Environment` working, it's time to implement evaluation of expressions
with variables.
"""


def test_evaluating_symbol():
    """TEST 4.8: Symbols (other than #t and #f) are treated as variable references.

    When evaluating a symbol, the corresponding value should be looked up in the
    environment.
    """

    env = Environment({"foo": 42})
    assert_equals(42, evaluate("foo", env))


def test_lookup_missing_variable():
    """TEST 4.9: Referencing undefined variables should raise an appropriate exception.

    This test should already be working if you implemented the environment correctly.
    """

    with assert_raises_regexp(DiyLangError, "my-var"):
        evaluate("my-var", Environment())


def test_define():
    """TEST 4.10: Test of simple define statement.

    The `define` form is used to define new bindings in the environment.
    A `define` call should result in a change in the environment. What you
    return from evaluating the definition is not important (although it
    affects what is printed in the REPL).
    """

    env = Environment()
    evaluate(parse("(define x 1000)"), env)
    assert_equals(1000, env.lookup("x"))


def test_define_with_wrong_number_of_arguments():
    """TEST 4.11: Defines should have exactly two arguments, or raise an error.

    This type of check could benefit the other forms we implement as well,
    and you might want to add them elsewhere. It quickly get tiresome to
    test for this however, so the tests won't require you to.
    """

    with assert_raises_regexp(DiyLangError, "Wrong number of arguments"):
        evaluate(parse("(define x)"), Environment())

    with assert_raises_regexp(DiyLangError, "Wrong number of arguments"):
        evaluate(parse("(define x 1 2)"), Environment())


def test_define_with_nonsymbol_as_variable():
    """TEST 4.12: Defines require the first argument to be a symbol."""

    with assert_raises_regexp(DiyLangError, "not a symbol"):
        evaluate(parse("(define #t 42)"), Environment())

def test_define_with_nonsymbol_as_variable():
    """TEST 4.13: Defines should evaluate the argument before storing it in
    the environment.
    """

    env = Environment()
    evaluate(parse("(define x (+ 1 41))"), env)
    assert_equals(42, env.lookup("x"))


def test_variable_lookup_after_define():
    """TEST 4.14: Test define and lookup variable in same environment.

    This test should already be working when the above ones are passing.
    """

    env = Environment()
    evaluate(parse("(define foo (+ 2 2))"), env)
    assert_equals(4, evaluate("foo", env))
