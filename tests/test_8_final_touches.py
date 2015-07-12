# -*- coding: utf-8 -*-

from nose.tools import assert_equals, assert_is_instance, assert_raises_regexp
from nose.plugins.skip import SkipTest
from os.path import dirname, relpath, join

from diylisp.interpreter import interpret, interpret_file
from diylisp.types import Environment, String, LispError
from diylisp.parser import parse

env = Environment()
path = join(dirname(relpath(__file__)), '..', 'stdlib.diy')
interpret_file(path, env)

"""
In this last part, we provide tests for some suggestions on how to improve
the language a bit. Treat these tasks as optional, and suggestions only.
Feel free to do something completely different, if you fancy.
"""

"""
Suggestion 1: `cond`

First off, we will implement a new control structure found in most Lisps, the 
`cond` form (not to be confused with `cons`). The name `cond` is short for 
"conditional", and is sort of an buffed up version of `if`.

Implement this as a new case in the `evaluate` function in `evaluator.py`.
"""


def test_cond_returns_right_branch():
    """
    `cond` takes as arguments an variable a list of tuples (two-element lists, 
    or "conses").

    The first element of each tuple is evaluated in order, until noe evaluates 
    to `#t`. The second element of that tuple is returned. 
    """

    program = """
    (cond ((#f 'foo)
           (#t 'bar)
           (#f 'baz)))
    """
    assert_equals("bar", interpret(program, env))

def test_cond_dosnt_evaluate_all_branches():
    """
    Of all the second tuple elements, only the one we return is ever evaluated.
    """

    interpret("(define foo 42)", env)

    program = """
    (cond ((#f fire-the-missiles)
           (#t foo)
           (#f something-else-we-wont-do)))
    """
    assert_equals("42", interpret(program, env))

def test_cond_not_evaluating_more_predicateds_than_neccessary():
    """
    Once we find an predicate that evaluates to `#t`, no more predicates should
    be evaluated.
    """

    program = """
    (cond ((#f 1)
           (#t 2)
           (dont-evaluate-me! 3)))
    """
    assert_equals("2", interpret(program, env))

def test_cond_evaluates_predicates():
    """
    Remember to evaluate the predicates before checking whether they are true.
    """

    program = """
    (cond (((not #t) 'totally-not-true)
           ((> 4 3) 'tru-dat)))
    """

    assert_equals("tru-dat", interpret(program, env))

def test_cond_returnes_false_as_default():
    """
    If we evalaute all the predicates, only to find that none of them turned out 
    to be true, then `cond` should return `#f`.
    """

    program = """
    (cond ((#f 'no)
           (#f 'nope)
           (#f 'i-dont-even)))
    """

    assert_equals("#f", interpret(program, env))


"""
Suggestion 2: Strings

So far, our new language have been missing a central data type, one that no
real language could do without -- strings. So, lets add them to the language.
"""

def test_parsing_simple_strings():
    """
    First things first, we need to be able to parse the strings.

    Since we already use python strings for our symbols, we need something else.
    Lets use a simple data type, `String`, which you will (rather conveniently)
    find ready made in the file `types.py`.

    > Side note:
    > 
    > This is where it starts to show that we could have used smarter 
    > representation of our types. We wanted to keep things simple early on, 
    > and now we pay the price. We could have represented our types as tuples 
    > of type and value, or perhaps made classes for all of them.
    >
    > Feel free to go back and fix this. Refactor as much as you wish -- just
    > remember to update the tests accordingly.
    """

    ast = parse('"foo bar"')
    assert_is_instance(ast, String) 
    assert_equals("foo bar", ast.val)

def test_parsing_strings_with_escaped_double_quotes():
    """
    We should be able to create strings with "-characters by escaping them.
    """

    ast = parse('"Say \\"what\\" one more time!"')

    assert_is_instance(ast, String) 
    assert_equals('Say \\"what\\" one more time!', ast.val)

def test_parsing_unclosed_strings():
    """
    Strings that are not closed result in an parse error.
    """

    with assert_raises_regexp(LispError, 'Unclosed string'):
        parse('"hey, close me!')

def test_parsing_strings_are_closed_by_first_closing_quotes():
    """
    Strings are delimited by the first and last (unescaped) double quotes.

    Thus, unescaped quotes followed by anything at all should be considered
    invalid and throw an exception.
    """

    with assert_raises_regexp(LispError, 'Expected EOF'):
        parse('"foo" bar"')

def test_evaluating_strings():
    """
    Strings is one of the basic data types, and thus an atom. Strings should
    therefore evaluate to themselves.

    Update the `is_atom` function in `ast.py` to make this happen.
    """

    random_quote = '"The limits of my language means the limits of my world."'

    assert_equals(random_quote, interpret(random_quote, env))

def test_empty_strings_behave_as_empty_lists():
    """
    It is common in many languages for strings to behave as lists. This can be
    rather convenient, so let's make it that way here as well.

    We have four basic list functions: `cons`, `head`, `tail` and `empty`.

    To take the easy one first: `empty` should only return `#t` for the empty
    string (and empty lists, as before).
    """

    assert_equals("#t", interpret('(empty "")'))
    assert_equals("#f", interpret('(empty "not empty")'))

def test_strings_have_heads_and_tails():
    """
    Next, `head` and `tail` needs to extract the first character and the rest
    of the charactes, respectively, from the string.
    """

    assert_equals('"f"', interpret('(head "foobar")'))
    assert_equals('"oobar"', interpret('(tail "foobar")'))

def test_consing_strings_back_together():
    """
    Finally, we need to be able to reconstruct a strings from its head and tail
    """

    assert_equals('"foobar"', interpret('(cons "f" "oobar")'))


"""
Suggestion 3: `let`
"""

"""
Suggestion 4: `defn`
"""

"""
Suggestion 5: IO
"""
