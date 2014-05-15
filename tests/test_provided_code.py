# -*- coding: utf-8 -*-

from nose.tools import assert_equals, assert_raises_regexp, assert_raises

from diylisp.parser import unparse, find_matching_paren
from diylisp.types import LispError

"""
This module contains a few tests for the code provided for part 1.
All tests here should already pass, and should be of no concern to
you as a workshop attendee.
"""

## Tests for find_matching_paren function in parser.py


def test_find_matching_paren():
    source = "(foo (bar) '(this ((is)) quoted))"
    assert_equals(32, find_matching_paren(source, 0))
    assert_equals(9, find_matching_paren(source, 5))


def test_find_matching_empty_parens():
    assert_equals(1, find_matching_paren("()", 0))


def test_find_matching_paren_throws_exception_on_bad_initial_position():
    """If asked to find closing paren from an index where there is no opening
    paren, the function should raise an error"""

    with assert_raises(AssertionError):
        find_matching_paren("string without parens", 4)


def test_find_matching_paren_throws_exception_on_no_closing_paren():
    """The function should raise error when there is no matching paren to be found"""

    with assert_raises_regexp(LispError, "Incomplete expression"):
        find_matching_paren("string (without closing paren", 7)

## Tests for unparse in parser.py


def test_unparse_atoms():
    assert_equals("123", unparse(123))
    assert_equals("#t", unparse(True))
    assert_equals("#f", unparse(False))
    assert_equals("foo", unparse("foo"))


def test_unparse_list():
    assert_equals("((foo bar) baz)", unparse([["foo", "bar"], "baz"]))


def test_unparse_quotes():
    assert_equals("''(foo 'bar '(1 2))", unparse(
        ["quote", ["quote", ["foo", ["quote", "bar"], ["quote", [1, 2]]]]]))


def test_unparse_bool():
    assert_equals("#t", unparse(True))
    assert_equals("#f", unparse(False))


def test_unparse_int():
    assert_equals("1", unparse(1))
    assert_equals("1337", unparse(1337))
    assert_equals("-42", unparse(-42))


def test_unparse_symbol():
    assert_equals("+", unparse("+"))
    assert_equals("foo", unparse("foo"))
    assert_equals("lambda", unparse("lambda"))


def test_unparse_another_list():
    assert_equals("(1 2 3)", unparse([1, 2, 3]))
    assert_equals("(if #t 42 #f)",
                  unparse(["if", True, 42, False]))


def test_unparse_other_quotes():
    assert_equals("'foo", unparse(["quote", "foo"]))
    assert_equals("'(1 2 3)",
                  unparse(["quote", [1, 2, 3]]))


def test_unparse_empty_list():
    assert_equals("()", unparse([]))
