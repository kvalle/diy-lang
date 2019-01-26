# -*- coding: utf-8 -*-

from nose.tools import assert_equals, assert_true, assert_raises_regexp

from diylang.ast import is_integer
from diylang.parser import parse, unparse
from diylang.types import DiyLangError


def test_parse_single_symbol():
    """TEST 1.1: Parsing a single symbol.

    Symbols are represented by text strings. Parsing a single atom should
    result in an AST consisting of only that symbol."""

    assert_equals('foo', parse('foo'))


def test_parse_boolean():
    """TEST 1.2: Parsing single booleans.

    Booleans are the special symbols #t and #f. In the ASTs they are
    represented by Python's True and False, respectively."""

    assert_equals(True, parse('#t'))
    assert_equals(False, parse('#f'))


def test_parse_integer():
    """TEST 1.3: Parsing single integer.

    Integers are represented in the ASTs as Python ints.

    Tip: String objects have a handy .isdigit() method.
    """

    assert_equals(42, parse('42'))
    assert_equals(1337, parse('1337'))
    assert_true(is_integer(parse('42')),
        "Numbers should be represented as integers in the AST")


def test_parse_list_of_symbols():
    """TEST 1.4: Parsing list of only symbols.

    A list is represented by a number of elements surrounded by parens. Python
    lists are used to represent lists as ASTs.

    Tip: The useful helper function `find_matching_paren` is already provided
    in `parse.py`.
    """

    assert_equals(['foo', 'bar', 'baz'], parse('(foo bar baz)'))
    assert_equals([], parse('()'))


def test_parse_list_of_mixed_types():
    """TEST 1.5: Parsing a list containing different types.

    When parsing lists, make sure each of the sub-expressions are also parsed
    properly."""

    assert_equals(['foo', True, 123], parse('(foo #t 123)'))


def test_parse_on_nested_list():
    """TEST 1.6: Parsing should also handle nested lists properly."""

    program = '(foo (bar ((#t)) x) (baz y))'
    ast = ['foo',
           ['bar', [[True]], 'x'],
           ['baz', 'y']]
    assert_equals(ast, parse(program))


def test_parse_exception_missing_paren():
    """TEST 1.7: The proper exception should be raised if the expression
    is incomplete."""

    with assert_raises_regexp(DiyLangError, 'Incomplete expression'):
        parse('(foo (bar x y)')


def test_parse_exception_extra_paren():
    """TEST 1.8: Another exception is raised if the expression is too large.

    The parse function expects to receive only one single expression. Anything
    more than this, should result in the proper exception."""

    with assert_raises_regexp(DiyLangError, 'Expected EOF'):
        parse('(foo (bar x y)))')


def test_parse_with_extra_whitespace():
    """TEST 1.9: Excess whitespace should be removed.

    Tip: String objects have a handy .strip() method.
    """

    program = """

       (program    with   much        whitespace)
    """
    expected_ast = ['program', 'with', 'much', 'whitespace']
    assert_equals(expected_ast, parse(program))


def test_parse_comments():
    """TEST 1.10: All comments should be stripped away as part of
    the parsing."""

    program = """
    ;; this first line is a comment
    (define variable
        ; here is another comment
        (if #t
            42 ; inline comment!
            (something else)))
    """
    expected_ast = ['define', 'variable',
                    ['if', True,
                     42,
                     ['something', 'else']]]
    assert_equals(expected_ast, parse(program))


def test_parse_larger_example():
    """TEST 1.11: Test a larger example to check that everything works
    as expected"""

    program = """
        (define fact
        ;; Factorial function
        (lambda (n)
            (if (<= n 1)
                1 ; Factorial of 0 is 1, and we deny
                  ; the existence of negative numbers
                (* n (fact (- n 1))))))
    """
    ast = ['define', 'fact',
           ['lambda', ['n'],
            ['if', ['<=', 'n', 1],
             1,
             ['*', 'n', ['fact', ['-', 'n', 1]]]]]]
    assert_equals(ast, parse(program))

# The following tests checks that quote expansion works properly


def test_expand_single_quoted_symbol():
    """TEST 1.12: Quoting is a shorthand syntax for calling the `quote` form.

    Examples:

        'foo -> (quote foo)
        '(foo bar) -> (quote (foo bar))

    """
    assert_equals(["foo", ["quote", "nil"]], parse("(foo 'nil)"))


def test_nested_quotes():
    """TEST 1.13: Nested quotes should work as expected"""
    assert_equals(["quote", ["quote", ["quote", ["quote", "foo"]]]],
                  parse("''''foo"))


def test_expand_crazy_quote_combo():
    """TEST 1.14: One final test to see that quote expansion works."""

    source = "'(this ''''(makes ''no) 'sense)"
    assert_equals(source, unparse(parse(source)))
