# -*- coding: utf-8 -*-

from nose.tools import assert_equals, assert_raises_regexp, \
    assert_raises, assert_false, assert_is_instance

from diylisp.interpreter import interpret
from diylisp.evaluator import evaluate
from diylisp.parser import parse
from diylisp.types import LispError, Environment

def test_creating_lists_by_quoting():
    """One way to create lists is by quoting.

    We have already implemented `quote` so this test should already be
    passing.

    The reason we need to use `quote` here is that otherwise the expression would
    be seen as a call to the first element -- `1` in this case, which obviously isn't
    even a function."""

    assert_equals([1, 2, 3, True], evaluate(parse("'(1 2 3 #t)"), Environment()))

def test_creating_list_with_cons():
    """The `cons` functions prepends an element to the front of a list."""

    result = evaluate(parse("(cons 0 '(1 2 3))"), Environment())
    assert_equals(parse("(0 1 2 3)"), result)

def test_creating_list_with_one_element():
    """`cons` should treat the symbol 'nil as the empty list."""

    result = evaluate(parse("(cons 42 'nil)"), Environment())
    assert_equals(parse("(42)"), result)

def test_creating_longer_lists_with_only_cons():
    """`cons` needs to evaluate it's arguments.

    Like all the other special forms and functions in our language, `cons` is 
    call-by-value. This means that the arguments must be evaluated before we 
    create the list with their values."""

    result = evaluate(parse("(cons 3 (cons (- 4 2) (cons 1 'nil)))"), Environment())
    assert_equals(parse("(3 2 1)"), result)

def test_deconstructing_list_with_car_and_cdr():
    """"""
    pass

#def test_deconstruction_of_lists():
#    """Tests picking elements from lists using car and cdr."""
#
#    env = Environment()
#    interpret("(define lst (list 1 2 3 4 5))", env)
#    assert_equals("1", interpret("(car lst)", env))
#    assert_equals("2", interpret("(car (cdr lst))", env))
#    assert_equals("(3 4 5)", interpret("(cdr (cdr lst))", env))
