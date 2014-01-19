# -*- coding: utf-8 -*-

from nose.tools import assert_equals, assert_raises_regexp

from diylisp.parser import parse, unparse
from diylisp.types import LispError

def test_parse_single_symbol():
    """Parsing a single symbol.

    Symbols are represented by text strings. Parsing a single atom should result
    in an AST consisting of only that symbol."""

    assert_equals('foo', parse('foo'))

def test_parse_boolean():
    """Parsing single booleans.

    Booleans are the special symbols #t and #f. In the ASTs they are represented 
    by Pythons True and False, respectively. """

    assert_equals(True, parse('#t'))
    assert_equals(False, parse('#f'))

def test_parse_integer():
    """Parsing single integer.

    Integers are represented in the ASTs as Python ints.

    Tip: String objects have a handy .isdigit() method.
    """

    assert_equals(42, parse('42'))
    assert_equals(1337, parse('1337'))

def test_parse_list_of_symbols():
    """Parsing list of only symbols.

    A list is represented by a number of elements surrounded by parens. Python lists 
    are used to represent lists as ASTs.

    Tip: The useful helper function `find_matching_paren` is already provided in
    `parse.py`.
    """

    assert_equals(['foo', 'bar', 'baz'], parse('(foo bar baz)'))
    assert_equals([], parse('()'))

def test_parse_list_of_mixed_types():
    """Parsing a list containing different types.

    When parsing lists, make sure each of the sub-expressions are also parsed 
    properly."""

    assert_equals(['foo', True, 123], parse('(foo #t 123)'))

def test_parse_on_nested_list():
    """Parsing should also handle nested lists properly."""

    program = '(foo (bar ((#t)) x) (baz y))'
    ast = ['foo', 
            ['bar', [[True]], 'x'], 
            ['baz', 'y']]
    assert_equals(ast, parse(program))

def test_parse_exception_missing_paren():
    """The proper exception should be raised if the expresions is incomplete."""

    with assert_raises_regexp(LispError, 'Incomplete expression'):
        parse('(foo (bar x y)')

def test_parse_exception_extra_paren():
    """Another exception is raised if the expression is too large.

    The parse function expects to recieve only one single expression. Anything
    more than this, should result in the proper exception."""

    with assert_raises_regexp(LispError, 'Expected EOF'):
        parse('(foo (bar x y)))')

def test_parse_comments():
    """All comments should be stripped away as part of the parsing."""

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
    """Test a larger example to check that everything works as expected"""

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

## The following tests checks that quote expansion works properly

def test_expand_single_quoted_symbol():
    """Quoting is a shorthand syntax for calling the `quote` form.

    Examples:

        'foo -> (quote foo)
        '(foo bar) -> (quote (foo bar))

    """
    assert_equals(["foo", ["quote", "nil"]], parse("(foo 'nil)"))

def test_nested_quotes():
    assert_equals(["quote", ["quote", ["quote", ["quote", "foo"]]]], parse("''''foo"))

def test_expand_crazy_quote_combo():
    """One final test to see that quote expansion works."""

    source = "'(this ''''(makes ''no) 'sense)"
    assert_equals(source, unparse(parse(source)))
