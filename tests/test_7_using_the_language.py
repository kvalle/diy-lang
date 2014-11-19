# -*- coding: utf-8 -*-

from nose.tools import assert_equals
from os.path import dirname, relpath, join

from diylisp.interpreter import interpret, interpret_file
from diylisp.types import Environment

env = Environment()
path = join(dirname(relpath(__file__)), '..', 'stdlib.diy')
interpret_file(path, env)

"""
Consider these tests as suggestions for what a standard library for
your language could contain. Each test function tests the implementation
of one stdlib function.

Put the implementation in the file `stdlib.diy` at the root directory
of the repository. The first function, `not` is already defined for you.
It's your job to create the rest, or perhaps somthing completely different?

Anything you put in `stdlib.diy` is also available from the REPL, so feel
free to test things out there.

    $ ./repl 
    →  (not #t)
    #f

PS: Note that in these tests, `interpret` is used. In addition to parsing 
and evaluating, it "unparses" the result, hence strings such as "#t" as the 
expected result instead of `True`.
"""


def test_not():
    assert_equals("#t", interpret('(not #f)', env))
    assert_equals("#f", interpret('(not #t)', env))


def test_or():
    assert_equals("#f", interpret('(or #f #f)', env))
    assert_equals("#t", interpret('(or #t #f)', env))
    assert_equals("#t", interpret('(or #f #t)', env))
    assert_equals("#t", interpret('(or #t #t)', env))


def test_and():
    assert_equals("#f", interpret('(and #f #f)', env))
    assert_equals("#f", interpret('(and #t #f)', env))
    assert_equals("#f", interpret('(and #f #t)', env))
    assert_equals("#t", interpret('(and #t #t)', env))


def test_xor():
    assert_equals("#f", interpret('(xor #f #f)', env))
    assert_equals("#t", interpret('(xor #t #f)', env))
    assert_equals("#t", interpret('(xor #f #t)', env))
    assert_equals("#f", interpret('(xor #t #t)', env))


# The language core just contains the > operator. 
# It's time to implement the rest.

def test_greater_or_equal():
    assert_equals("#f", interpret('(>= 1 2)', env))
    assert_equals("#t", interpret('(>= 2 2)', env))
    assert_equals("#t", interpret('(>= 2 1)', env))


def test_less_or_equal():
    assert_equals("#t", interpret('(<= 1 2)', env))
    assert_equals("#t", interpret('(<= 2 2)', env))
    assert_equals("#f", interpret('(<= 2 1)', env))


def test_less_than():
    assert_equals("#t", interpret('(< 1 2)', env))
    assert_equals("#f", interpret('(< 2 2)', env))
    assert_equals("#f", interpret('(< 2 1)', env))


# Lets also implement some basic list functions.
# These should be pretty easy with some basic recursion.

def test_length():
    """Count the number of element in the list.

    Tip: How many elements are there in the empty list?"""

    assert_equals("5", interpret("(length '(1 2 3 4 5))", env))
    assert_equals("3", interpret("(length '(#t '(1 2 3) 'foo-bar))", env))
    assert_equals("0", interpret("(length '())", env))


def test_sum():
    """Calculate the sum of all elements in the list."""

    assert_equals("5", interpret("(sum '(1 1 1 1 1))", env))
    assert_equals("10", interpret("(sum '(1 2 3 4))", env))
    assert_equals("0", interpret("(sum '())", env))

def test_range():
    """Output a list with a range of numbers.

    The two arguments define the bounds of the (inclusive) bounds of the range."""

    assert_equals("(1 2 3 4 5)", interpret("(range 1 5)", env))
    assert_equals("(1)", interpret("(range 1 1)", env))
    assert_equals("()", interpret("(range 2 1)", env))


def test_append():
    """Append should merge two lists together."""

    assert_equals("()", interpret("(append '() '())", env))
    assert_equals("(1)", interpret("(append '() '(1))", env))
    assert_equals("(2)", interpret("(append '(2) '())", env))
    assert_equals("(1 2 3 4 5)", interpret("(append '(1 2) '(3 4 5))", env))
    assert_equals("(#t #f 'maybe)", interpret("(append '(#t) '(#f 'maybe))", env))


def test_reverse():
    """Reverse simply outputs the same list with elements in reverse order.

    Tip: See if you might be able to utilize the function you just made."""

    assert_equals("()", interpret("(reverse '())", env))
    assert_equals("(1)", interpret("(reverse '(1))", env))
    assert_equals("(4 3 2 1)", interpret("(reverse '(1 2 3 4))", env))


# Next, our standard library should contain the three most fundamental functions:
# `filter`, `map` and `reduce`.

def test_filter():
    """Filter removes any element not satisfying a predicate from a list."""

    interpret("""
        (define even
            (lambda (x)
                (eq (mod x 2) 0)))
    """, env)
    assert_equals("(2 4 6)", interpret("(filter even '(1 2 3 4 5 6))", env))


def test_map():
    """Map applies a given function to all elements of a list."""

    interpret("""
        (define inc
            (lambda (x) (+ 1 x)))
    """, env)
    assert_equals("(2 3 4)", interpret("(map inc '(1 2 3))", env))


def test_reduce():
    """Reduce, also known as fold, reduce a list into a single value.

    It does this by combining elements two by two, untill there is only
    one left.

    If this is unfamiliar to you, have a look at:
    http://en.wikipedia.org/wiki/Fold_(higher-order_function)"""

    interpret("""
        (define max 
            (lambda (a b) 
                (if (> a b) a b)))
    """, env)

    # Evaluates as (max 1 (max 6 (max 3 (max 2 0)))) -> 6
    assert_equals("6", interpret("(reduce max 0 '(1 6 3 2))", env))


    interpret("""
        (define add 
            (lambda (a b) (+ a b)))
    """, env)

    # Lets see if we can improve a bit on `sum` while we're at it
    assert_equals("10", interpret("(reduce add 0 (range 1 4))", env))


# Finally, no stdlib is complete without a sorting algorithm.
# Quicksort or mergesort might be good options, but you choose which 
# ever one you prefer.

# You might want to implement a few helper functions for this one.

def test_sort():
    assert_equals("()", interpret("'()", env))
    assert_equals("(1)", interpret("'(1)", env))
    assert_equals("(1 2 3 4 5 6 7)",
                  interpret("(sort '(6 3 7 2 4 1 5))", env))
    assert_equals("(1 2 3 4 5 6 7)",
                  interpret("(sort '(1 2 3 4 5 6 7))", env))
    assert_equals("(1 2 3 4 5 6 7)",
                  interpret("(sort '(7 6 5 4 3 2 1))", env))
    assert_equals("(1 1 1)",
                  interpret("(sort '(1 1 1))", env))
