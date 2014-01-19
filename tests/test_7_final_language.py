# -*- coding: utf-8 -*-

from nose.tools import assert_equals

from diylisp.interpreter import interpret
from diylisp.types import Environment

class TestDIYLisp:
    """Testing the implementation with a few non-trivial programs"""

    def test_factorial(self):
        """Simple factorial"""
        env = Environment()
        interpret("""
            (define fact
                (lambda (n)
                    (if (eq n 0)
                        1 
                        (* n (fact (- n 1))))))
        """, env)
        assert_equals("120", interpret("(fact 5)", env))

    def test_gcd(self):
        """Greates common dividor"""
        env = Environment()
        interpret("""
            (define gcd
                (lambda (a b)
                    (if (eq b 0)
                        a 
                        (gcd b (mod a b)))))
        """, env)
        assert_equals("6", interpret("(gcd 108 30)", env))
        assert_equals("1", interpret("(gcd 17 5)", env))
