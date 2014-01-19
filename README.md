## DIY Lisp (batteries included, some assembly required)

In this tutorial/workshop we'll be implementing our own little language, more or less from scratch.

We will make a relatively simple, but neat, language. We aim for the following features:

- A handful of datatypes (integers, booleans and symbols)
- First order functions with lexical scoping
- That nice homemade quality feeling

We will not have:

- A proper type system
- Error handling
- Good performance
- And much more

### Setup

To get up and running, make sure you have installed [Python](http://www.python.org/) and [Pip](https://pypi.python.org/pypi/pip). Then install the requirements:

    pip install -r requirements.txt

If your are familiar with [virtualenv](http://www.virtualenv.org/en/latest/) you might want to do this in a separate pyenv.


### Goal

By the end of the tutorial you will have implemented a simple programming language, and will hopefully have understood languages better on a fundamental level. 

The language should be able to interpret the following code by the time we are done:

```lisp
;; Some example lisp code. By the end of the tutorial, our Lisp will be
;; able to run this.

;; To run the code:
;;
;;    ./diy example.diy
;;

(define fact 
    ;; Factorial function
    (lambda (n) 
        (if (<= n 1) 
            1 ; Factorial of 0 is 1, and we deny 
              ; the existence of negative numbers
            (* n (fact (- n 1))))))

;; When parsing the file, the last statement is returned
(fact 5)
```

### Part 1 - parsing

The job of the `parse` step is to convert the program represented as a string into a representation we can work with in the `evaluate` step.

This representation, called the abstract syntax tree (AST), will look like this for our language:


```python
>>> from diylisp.parser import parse
>>> program = """
...   (define fact 
...       ;; Factorial function
...       (lambda (n) 
...           (if (eq n 0) 
...               1 ; Factorial of 0 is 1, and we deny 
...                 ; the existence of negative numbers
...               (* n (fact (- n 1))))))
... """))
>>> parse(program)
['define', 'fact', ['lambda', ['n'], ['if', ['eq', 'n', 0], 1, ['*', 'n', ['fact', ['-', 'n', 1]]]]]]
```

- Comments are removed.
- Symbols are represented as strings.
- The lisp list expressions are represented as Python lists.
- The symbols `#t` and `#f` are represented by Pythons `True` and `False, respectively.
- Integers are represented as Python integers.

The parsing is done in `parsing.py`. It is your job to implement the `parse` function.
A lot of the gritty work of counting parentheses and such has been done for you, but you must stitch everything together.

Have a look at the provided functions in the module, and start working. Run the following command until all tests pass.

    nosetests tests/test_1_parsing.py --stop

