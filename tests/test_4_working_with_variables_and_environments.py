# -*- coding: utf-8 -*-

from nose.tools import assert_equals, assert_raises_regexp

from diylisp.types import LispError, Environment
from diylisp.evaluator import evaluate
from diylisp.interpreter import interpret

def test_evaluating_symbol():
    """Symbols (other than #t and #f) are treated as variable references.

    When evaluating a symbol, the corresponding value should be looked up in the 
    environment."""

    env = Environment({"foo": 42})
    assert_equals(42, evaluate("foo", env))

class TestEval:

    # Test working with environments

    def test_simple_lookup_from_env(self):
        env = Environment({"foo": 42, "bar": True})
        assert_equals(42, evaluate("foo", env))

    def test_lookup_missing_variable(self):
        with assert_raises_regexp(LispError, "my-var"):
            evaluate("my-var", Environment())

    def test_define(self):
        """Test simplest possible define"""

        env = Environment()
        evaluate(["define", "x", 1000], env)
        assert_equals(1000, env.lookup("x"))

    def test_define_with_wrong_number_of_arguments(self):
        """Defines should have exactly two arguments, or raise an error"""

        with assert_raises_regexp(LispError, "Wrong number of arguments"):
            evaluate(["define", "x"], Environment())

        with assert_raises_regexp(LispError, "Wrong number of arguments"):
            evaluate(["define", "x", 1, 2], Environment())

    def test_define_with_nonsymbol_as_variable(self):
        """Malformed defines should throw an error"""

        with assert_raises_regexp(LispError, "non-symbol"):
            evaluate(["define", True, 42], Environment())


class TestEnvironment:

    def test_simple_lookup(self):
        env = Environment({"var": 42})
        assert_equals(42, env.lookup("var"))

    def test_lookup_from_inner_env(self):
        env = Environment({"var": 42})
        env.extend({"foo": "bar"})
        assert_equals(42, env.lookup("var"))

    def test_lookup_deeply_nested_var(self):
        env = Environment({"a": 1}).extend({"b": 2}).extend({"c": 3}).extend({"foo": 100})
        assert_equals(100, env.lookup("foo"))

    def test_lookup_on_missing_raises_exception(self):
        """When looking up an undefined symbol, an error should be raised.

        The error message should contain the relevant symbol, and inform that it has 
        not been defined."""
        
        with assert_raises_regexp(LispError, "my-missing-var"):
            Environment().lookup("my-missing-var")

    def test_extend_returns_new_environment(self):
        """The extend method should create a new environment, leaving the old one unchanged."""
        env = Environment({"foo": 1})
        extended = env.extend({"foo": 2})

        assert_equals(1, env.lookup("foo"))
        assert_equals(2, extended.lookup("foo"))

    def test_set_changes_environment_in_place(self):
        """When calling `set` the environment should be updated"""

        env = Environment({"foo": 1})
        env.set("foo", 2)
        assert_equals(2, env.lookup("foo"))
