# -*- coding: utf-8 -*-

from nose.tools import assert_equals, assert_raises_regexp, \
    assert_raises, assert_false, assert_is_instance

from diylisp.interpreter import interpret
from diylisp.evaluator import evaluate
from diylisp.parser import parse
from diylisp.types import LispError, Environment

class TestBuiltins:

    def setup(self):
        self.env = Environment()

    def test_creating_lists(self):
        """Test different ways to create lists"""

        xs = "(1 2 #t 4)"
        assert_equals(xs, interpret("(quote (1 2 #t 4))", self.env))
        assert_equals(xs, interpret("(cons 1 (cons 2 (cons #t (cons 4 '()))))", self.env))
        assert_equals(xs, interpret("(list 1 2 #t 4)", self.env))

    def test_deconstruction_of_lists(self):
        """Tests picking elements from lists using car and cdr"""

        interpret("(define lst (list 1 2 3 4 5))", self.env)
        assert_equals("1", interpret("(car lst)", self.env))
        assert_equals("2", interpret("(car (cdr lst))", self.env))
        assert_equals("(3 4 5)", interpret("(cdr (cdr lst))", self.env))
