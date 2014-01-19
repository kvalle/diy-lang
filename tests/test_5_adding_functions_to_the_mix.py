# -*- coding: utf-8 -*-

from nose.tools import assert_equals, assert_raises_regexp, \
    assert_raises, assert_false, assert_is_instance

from diylisp.interpreter import interpret
from diylisp.evaluator import evaluate
from diylisp.parser import parse
from diylisp.types import Closure, LispError, Environment

def test_lambda_evaluates_to_lambda():
    """The lambda form should evaluate to a Closure"""

    ast = ["lambda", [], 42]
    closure = evaluate(ast, Environment())
    assert_is_instance(closure, Closure) 

def test_lambda_closure_keeps_defining_env():
    """The closure should keep a copy of the environment where it was defined"""

    env = Environment({"foo": 1, "bar": 2})
    ast = ["lambda", [], 42]
    closure = evaluate(ast, env)
    assert_equals(closure.env, env) 

def test_lambda_closure_holds_function():
    """The function part of the closure is the parameters and the body"""

    params = ["x", "y"]
    body = ["+", "x", "y"]
    ast = ["lambda", params, body]
    closure = evaluate(ast, Environment)
    assert_equals(closure.params, params)
    assert_equals(closure.body, body)

def test_call_to_non_function():
    """Should raise a TypeError when a non-closure is called as a function"""
    
    with assert_raises(LispError):
        evaluate([True, 1, 2], Environment())
    with assert_raises(LispError):
        evaluate(["foo", 1, 2], Environment({"foo": 42}))

def test_calling_with_wrong_number_of_arguments():
    """Lambda should raise exception when called with wrong number of arguments"""

    env = Environment()
    evaluate(["define", "fn", ["lambda", ["x", "y"], 42]], env)
    with assert_raises_regexp(LispError, "expected 2"):
        evaluate(["fn", 1], env)

def test_calling_simple_function():
    assert_equals(42, evaluate([["lambda", [], 42]], Environment()))

def test_defining_lambda_with_error():
    """Tests that the lambda body is not being evaluated when the lambda
    is evaluated or defined. (It should first be evaluated when the function
    is later invoced.)"""

    ast = parse("""
        (define fn-with-error
            (lambda (x y)
                (function body that would never work)))
    """)
    evaluate(ast, Environment())

def test_lambda_with_free_var():
    """Tests that the lambda have access to variables 
    from the environment in which it was defined"""

    env = Environment({"free-variable": 100})
    ast = [["lambda", [], "free-variable"]]
    assert_equals(100, evaluate(ast, env))

def test_lambda_with_argument():
    """Test that the arguments are included in the environment when 
    the function body is evaluated"""

    ast = [["lambda", ["x"], "x"], 42]
    assert_equals(42, evaluate(ast, Environment()))

def test_lambda_with_argument_and_env():
    """Test that arguments overshadow variables defined in the environment
    when the function body is evaluated"""

    env = Environment({"x": 1})
    ast = [["lambda", ["x"], "x"], 2]
    assert_equals(2, evaluate(ast, env))

def test_defining_then_looking_up_function():
    """Test calling named function that's been previously defined 
    from the environment"""

    env = Environment()
    evaluate(["define", "my-fn", ["lambda", ["x"], "x"]], env)
    assert_equals(42, evaluate(["my-fn", 42], env))

def test_calling_function_recursively():
    """Tests that a named function is included in the environment
    where it is evaluated"""
    
    oposite = """
        (define oposite
            (lambda (p) 
                (if p #f #t)))
    """
    fn = """ 
        (define fn 
            ;; Meaningless (albeit recursive) function
            (lambda (x) 
                (if x 
                    (fn (oposite x))
                    1000)))
    """
    
    env = Environment()
    evaluate(parse(oposite), env)
    evaluate(parse(fn), env)

    assert_equals(1000, evaluate(["fn", True], env))
    assert_equals(1000, evaluate(["fn", False], env))
    