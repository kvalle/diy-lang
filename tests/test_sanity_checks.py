# -*- coding: utf-8 -*-

from nose.tools import assert_equals

from diylisp.interpreter import interpret
from diylisp.types import Environment


def test_gcd():
    """Tests Greates Common Dividor (GCD)."""

    program = """
        (define gcd
            (lambda (a b)
                (if (eq b 0)
                    a 
                    (gcd b (mod a b)))))
    """

    env = Environment()
    interpret(program, env)

    assert_equals("6", interpret("(gcd 108 30)", env))
    assert_equals("1", interpret("(gcd 17 5)", env))
