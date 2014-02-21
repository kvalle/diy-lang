# -*- coding: utf-8 -*-

from nose.tools import assert_equals
from os.path import dirname, relpath, join

from diylisp.interpreter import interpret
from diylisp.types import Environment

def get_program(filename):
    """Helper function to read programs from file"""

    path = join(dirname(relpath(__file__)), "lisp", filename)
    with open(path, 'r') as f:
        return "".join(f.readlines())

def test_gcd():
    """Implement a function to calculate the Greatest Common Divisor. 

    The Greates Common Dividor (GCD) of two numbers `a` and `b` is 
    - `a` if `b` is 0
    - the gcd of `b` and "a mod b" otherwise

    Put your implementation of the `gcd` function in `tests/lisp/gcd.diy`.
    """

    env = Environment()
    interpret(get_program('gcd.diy'), env)

    assert_equals("6", interpret("(gcd 108 30)", env))
    assert_equals("1", interpret("(gcd 17 5)", env))
