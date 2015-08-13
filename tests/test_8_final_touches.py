# -*- coding: utf-8 -*-

from os.path import dirname, relpath, join

from nose.plugins.skip import SkipTest
from nose.tools import assert_true, assert_equals, assert_is_instance, \
    assert_raises_regexp, with_setup

from diylisp.interpreter import interpret, interpret_file
from diylisp.types import Environment, String, LispError, Closure
from diylisp.parser import parse

env = None

def prepare_env():
    global env
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
"conditional", and is sort of a buffed up version of `if`.

Implement this as a new case in the `evaluate` function in `evaluator.py`.
"""

@with_setup(prepare_env)
def test_cond_returns_right_branch():
    """
    `cond` takes as arguments a list of tuples (two-element lists, or "conses").

    The first element of each tuple is evaluated in order, until one evaluates 
    to `#t`. The second element of that tuple is returned.
    """

    program = """
    (cond ((#f 'foo)
           (#t 'bar)
           (#f 'baz)))
    """
    assert_equals("bar", interpret(program, env))

@with_setup(prepare_env)
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

@with_setup(prepare_env)
def test_cond_not_evaluating_more_predicateds_than_neccessary():
    """
    Once we find a predicate that evaluates to `#t`, no more predicates should
    be evaluated.
    """

    program = """
    (cond ((#f 1)
           (#t 2)
           (dont-evaluate-me! 3)))
    """
    assert_equals("2", interpret(program, env))

@with_setup(prepare_env)
def test_cond_evaluates_predicates():
    """
    Remember to evaluate the predicates before checking whether they are true.
    """

    program = """
    (cond (((not #t) 'totally-not-true)
           ((> 4 3) 'tru-dat)))
    """

    assert_equals("tru-dat", interpret(program, env))

@with_setup(prepare_env)
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

So far, our new language has been missing a central data type, one that no
real language could do without -- strings. So, lets add them to the language.
"""

@with_setup(prepare_env)
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

@with_setup(prepare_env)
def test_parsing_empty_string():
    """
    Empty strings are strings too!
    """

    assert_equals('', parse('""').val)

@with_setup(prepare_env)
def test_parsing_strings_with_escaped_double_quotes():
    """
    We should be able to create strings with "-characters by escaping them.
    """

    ast = parse('"Say \\"what\\" one more time!"')

    assert_is_instance(ast, String) 
    assert_equals('Say \\"what\\" one more time!', ast.val)

@with_setup(prepare_env)
def test_parsing_unclosed_strings():
    """
    Strings that are not closed result in an parse error.
    """

    with assert_raises_regexp(LispError, 'Unclosed string'):
        parse('"hey, close me!')

@with_setup(prepare_env)
def test_parsing_strings_are_closed_by_first_closing_quotes():
    """
    Strings are delimited by the first and last (unescaped) double quotes.

    Thus, unescaped quotes followed by anything at all should be considered
    invalid and throw an exception.
    """

    with assert_raises_regexp(LispError, 'Expected EOF'):
        parse('"foo" bar"')

@with_setup(prepare_env)
def test_evaluating_strings():
    """
    Strings is one of the basic data types, and thus an atom. Strings should
    therefore evaluate to themselves.

    Update the `is_atom` function in `ast.py` to make this happen.
    """

    random_quote = '"The limits of my language means the limits of my world."'

    assert_equals(random_quote, interpret(random_quote, env))

@with_setup(prepare_env)
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

@with_setup(prepare_env)
def test_strings_have_heads_and_tails():
    """
    Next, `head` and `tail` needs to extract the first character and the rest
    of the charactes, respectively, from the string.
    """

    assert_equals('"f"', interpret('(head "foobar")'))
    assert_equals('"oobar"', interpret('(tail "foobar")'))

@with_setup(prepare_env)
def test_consing_strings_back_together():
    """
    Finally, we need to be able to reconstruct a string from its head and tail
    """

    assert_equals('"foobar"', interpret('(cons "f" "oobar")'))


"""
Suggestion 3: `let`

The `let` form enables us to make local bindings.

It takes two arguments. First a list of bindings, secondly an expression to be
evaluated within an environment where those bindings exist.
"""

@with_setup(prepare_env)
def test_let_returns_result_of_the_given_expression():
    """
    The result when evaluating a `let` binding is the evaluation of the 
    expression given as argument.

    Let's first try one without any bindings.
    """

    program = "(let () (if #t 'yep 'nope))"

    assert_equals("yep", interpret(program, env))

@with_setup(prepare_env)
def test_let_extends_environment():
    """
    The evaluation of the inner expression should have available the bindings
    provided within the first argument.
    """

    program = """
        (let ((foo (+ 1000 42)))
             foo)
    """

    assert_equals("1042", interpret(program, env))

@with_setup(prepare_env)
def test_let_bindings_have_access_to_previous_bindings():
    """
    Each new binding should have access to the previous bindings in the list
    """

    program = """
        (let ((foo 10)
              (bar (+ foo 5)))
             bar)
    """

    assert_equals("15", interpret(program, env))

@with_setup(prepare_env)
def test_let_bindings_overshadow_outer_environment():
    """
    Let bindings should shadow definitions in from outer environments
    """

    interpret("(define foo 1)", env)

    program = """
        (let ((foo 2))
             foo)
    """

    assert_equals("2", interpret(program, env))

@with_setup(prepare_env)
def test_let_bindings_do_not_affect_outer_environment():
    """
    After the let is evaluated, all of it's bindings are forgotten
    """

    interpret("(define foo 1)", env)

    assert_equals("2", interpret("(let ((foo 2)) foo)", env))
    assert_equals("1", interpret("foo", env))



"""
Suggestion 4: `defn`

So far, to define functions we have had to write

    (define my-function 
        (lambda (foo bar)
            'fuction-body-here))

It is a bit ugly to have to make a lambda every time you want a named function.

Let's add some syntactic sugar, shall we:

    (defn my-function (foo bar)
        'function-body-here)

"""

@with_setup(prepare_env)
def test_defn_binds_the_variable_just_like_define():
    """
    Like `define`, the `defn` form should bind a variable to the environment.

    This variable should be a closure, just like if we had defined a new
    variable using the old `define` + `lambda` syntax.
    """

    interpret("(defn foo (x) (> x 10))", env)

    assert_is_instance(env.lookup("foo"), Closure)

@with_setup(prepare_env)
def test_defn_result_in_the_correct_closure():
    """
    The closure created should be no different than from the old syntax.

    Remember: you should be able to reuse most of what you need from
    the `define` implementation. No need to do all the heavy lifting twice.
    """

    interpret("(defn foo-1 (x) (> x 10))", env)
    interpret("(define foo-2 (lambda (x) (> x 10)))", env)

    foo1 = env.lookup("foo-1")
    foo2 = env.lookup("foo-2")

    assert_equals(foo1.body, foo2.body)
    assert_equals(foo1.params, foo2.params)
    assert_equals(foo1.env, foo2.env)

