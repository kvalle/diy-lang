# -*- coding: utf-8 -*-

from nose.tools import assert_equals

from diylang.interpreter import interpret
from diylang.types import Environment

def test_gcd():
    """Tests Greates Common Dividor (GCD).

    This test is intended to run after you have completed the core of the
    language, just to make sure that everything is holding together.
    """

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
