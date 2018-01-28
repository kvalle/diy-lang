# -*- coding: utf-8 -*-

from nose.tools import assert_equals, assert_raises_regexp, \
    assert_raises, assert_true, assert_is_instance

from diylang.ast import is_list
from diylang.evaluator import evaluate
from diylang.parser import parse
from diylang.types import Closure, DiyLangError, Environment

"""
This part is all about defining and using functions.

We'll start by implementing the `lambda` form which is used to create function
closures.
"""


def test_lambda_evaluates_to_closure():
    """TEST 5.1: The lambda form should evaluate to a Closure

    Tip: You'll find the Closure class ready in types.py, just finish the
    constructor.
    """

    ast = ["lambda", [], 42]
    closure = evaluate(ast, Environment())
    assert_is_instance(closure, Closure)


def test_lambda_closure_keeps_defining_env():
    """TEST 5.2: The closure should keep a copy of the environment where it was
    defined.

    Once we start calling functions later, we'll need access to the environment
    from when the function was created in order to resolve all free variables.
    """

    env = Environment({"foo": 1, "bar": 2})
    ast = ["lambda", [], 42]
    closure = evaluate(ast, env)
    assert_equals(closure.env, env)


def test_lambda_closure_holds_function():
    """TEST 5.3: The closure contains the parameter list and function body
    too."""

    closure = evaluate(parse("(lambda (x y) (+ x y))"), Environment())

    assert_equals(["x", "y"], closure.params)
    assert_equals(["+", "x", "y"], closure.body)


def test_lambda_arguments_are_lists():
    """TEST 5.4: The parameters of a `lambda` should be a list."""

    closure = evaluate(parse("(lambda (x y) (+ x y))"), Environment())
    assert_true(is_list(closure.params))

    with assert_raises(DiyLangError):
        evaluate(parse("(lambda not-a-list (body of fn))"), Environment())


def test_lambda_number_of_arguments():
    """TEST 5.5: The `lambda` form should expect exactly two arguments."""

    with assert_raises_regexp(DiyLangError, "number of arguments"):
        evaluate(parse("(lambda (foo) (bar) (baz))"), Environment())


def test_defining_lambda_with_error_in_body():
    """TEST 5.6: The function body should not be evaluated when the lambda is
    defined.

    The call to `lambda` should return a function closure holding, among other
    things the function body. The body should not be evaluated before the
    function is called.
    """

    ast = parse("""
            (lambda (x y)
                (function body ((that) would never) work))
    """)
    assert_is_instance(evaluate(ast, Environment()), Closure)


"""
Now that we have the `lambda` form implemented, let's see if we can call some
functions.

When evaluating ASTs which are lists, if the first element isn't one of the
special forms we have been working with so far, it is a function call. The
first element of the list is the function, and the rest of the elements are
arguments.
"""


def test_evaluating_call_to_closure():
    """TEST 5.7: The first case we'll handle is when the AST is a list with an
    actual closure as the first element.

    In this first test, we'll start with a closure with no arguments and no
    free variables. All we need to do is to evaluate and return the function
    body.
    """

    closure = evaluate(parse("(lambda () (+ 1 2))"), Environment())
    ast = [closure]
    result = evaluate(ast, Environment())
    assert_equals(3, result)


def test_evaluating_call_to_closure_with_arguments():
    """TEST 5.8: The function body must be evaluated in an environment where
    the parameters are bound.

    Create an environment where the function parameters (which are stored in
    the closure) are bound to the actual argument values in the function call.
    Use this environment when evaluating the function body.

    Tip: The `zip` and `dict` functions should prove useful when constructing
    the new environment.
    """

    env = Environment()
    closure = evaluate(parse("(lambda (a b) (+ a b))"), env)
    ast = [closure, 4, 5]

    assert_equals(9, evaluate(ast, env))


def test_creating_closure_with_environment():
    """TEST 5.9: The function parameters must properly shadow the outer scope's
    bindings.

    When the same bindings exist in the environment and function parameters,
    the function parameters must properly overwrite the environment bindings.
    """

    env = Environment({"a": 42, "b": "foo"})
    closure = evaluate(parse("(lambda (a b) (+ a b))"), env)
    ast = [closure, 4, 5]

    assert_equals(9, evaluate(ast, env))


def test_call_to_function_should_evaluate_arguments():
    """TEST 5.10: Call to function should evaluate all arguments.

    When a function is applied, the arguments should be evaluated before being
    bound to the parameter names.
    """

    env = Environment()
    closure = evaluate(parse("(lambda (a) (+ a 5))"), env)
    ast = [closure, parse("(if #f 0 (+ 10 10))")]

    assert_equals(25, evaluate(ast, env))


def test_evaluating_call_to_closure_with_free_variables():
    """TEST 5.11: The body should be evaluated in the environment from the closure.

    The function's free variables, i.e. those not specified as part of the
    parameter list, should be looked up in the environment from where the
    function was defined. This is the environment included in the closure. Make
    sure this environment is used when evaluating the body.
    """

    closure = evaluate(parse("(lambda (x) (+ x y))"), Environment({"y": 1}))
    ast = [closure, 0]
    result = evaluate(ast, Environment({"y": 2}))
    assert_equals(1, result)


"""
Okay, now we're able to evaluate ASTs with closures as the first element. But
normally the closures don't just happen to be there all by themselves.
Generally we'll find some expression, evaluate it to a closure, and then
evaluate a new AST with the closure just like we did above.

(some-exp arg1 arg2 ...) -> (closure arg1 arg2 ...) -> result-of-function-call

"""


def test_calling_very_simple_function_in_environment():
    """TEST 5.12: A call to a symbol corresponds to a call to its value in the
    environment.

    When a symbol is the first element of the AST list, it is resolved to its
    value in the environment (which should be a function closure). An AST with
    the variables replaced with its value should then be evaluated instead.
    """

    env = Environment()
    evaluate(parse("(define add (lambda (x y) (+ x y)))"), env)
    assert_is_instance(env.lookup("add"), Closure)

    result = evaluate(parse("(add 1 2)"), env)
    assert_equals(3, result)


def test_calling_lambda_directly():
    """TEST 5.13: It should be possible to define and call functions directly.

    A lambda definition in the call position of an AST should be evaluated, and
    then evaluated as before.
    """

    ast = parse("((lambda (x) x) 42)")
    result = evaluate(ast, Environment())
    assert_equals(42, result)


def test_calling_complex_expression_which_evaluates_to_function():
    """TEST 5.14: Actually, all ASTs that are lists beginning with anything except
    atoms, or with a symbol, should be evaluated and then called.

    In this test, a call is done to the if-expression. The `if` should be
    evaluated, which will result in a `lambda` expression. The lambda is
    evaluated, giving a closure. The result is an AST with a `closure` as the
    first element, which we already know how to evaluate.
    """

    ast = parse("""
        ((if #f
             wont-evaluate-this-branch
             (lambda (x) (+ x y)))
         2)
    """)
    env = Environment({'y': 3})
    assert_equals(5, evaluate(ast, env))


"""
Now that we have the happy cases working, let's see what should happen when
function calls are done incorrectly.
"""


def test_calling_atom_raises_exception():
    """TEST 5.15: A function call to a non-function should result in an
    error."""

    with assert_raises_regexp(DiyLangError, "not a function"):
        evaluate(parse("(#t 'foo 'bar)"), Environment())
    with assert_raises_regexp(DiyLangError, "not a function"):
        evaluate(parse("(42)"), Environment())


def test_make_sure_arguments_to_functions_are_evaluated():
    """TEST 5.16: The arguments passed to functions should be evaluated

    We should accept parameters that are produced through function
    calls. If you are seeing stack overflows, e.g.

    RuntimeError: maximum recursion depth exceeded while calling a Python
    object

    then you should double-check that you are properly evaluating the passed
    function arguments.
    """

    env = Environment()
    res = evaluate(parse("((lambda (x) x) (+ 1 2))"), env)
    assert_equals(res, 3)


def test_calling_with_wrong_number_of_arguments():
    """TEST 5.17: Functions should raise exceptions when called with wrong
    number of arguments."""

    env = Environment()
    evaluate(parse("(define fn (lambda (p1 p2) 'whatever))"), env)
    error_msg = "wrong number of arguments, expected 2 got 3"
    with assert_raises_regexp(DiyLangError, error_msg):
        evaluate(parse("(fn 1 2 3)"), env)


def test_calling_nothing():
    """TEST 5.18: Calling nothing should fail (remember to quote empty data
    lists)"""

    with assert_raises(DiyLangError):
        evaluate(parse("()"), Environment())


def test_make_sure_arguments_are_evaluated_in_correct_environment():
    """Test 5.19: Function arguments should be evaluated in correct environment

    Function arguments should be evaluated in the environment where the
    function is called, and not in the environment captured by the function.
    """

    env = Environment({'x': 3})
    evaluate(parse("(define foo (lambda (x) x))"), env)
    env = env.extend({'x': 4})
    assert_equals(evaluate(parse("(foo (+ x 1))"), env), 5)


"""
One final test to see that recursive functions are working as expected.
The good news: this should already be working by now :)
"""


def test_calling_function_recursively():
    """TEST 5.20: Tests that a named function is included in the environment where
    it is evaluated.
    """

    env = Environment()
    evaluate(parse("""
        (define my-fn
            ;; A meaningless, but recursive, function
            (lambda (x)
                (if (eq x 0)
                    42
                    (my-fn (- x 1)))))
    """), env)

    assert_equals(42, evaluate(parse("(my-fn 0)"), env))
    assert_equals(42, evaluate(parse("(my-fn 10)"), env))
