## DIY Lisp (some assembly required)

In this tutorial/workshop we'll be implementing our own little language, more or less from scratch.

We will make a relatively simple, but neat, language. We aim for the following features:

- A handful of datatypes (integers, booleans and symbols)
- First order functions with lexical scoping

We will not have:
- Quoting or quasiquoting
- Error handling
- Proper types (or the ability to define new types from within the language)
- Macros
- much, much, more

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

TODO: describe the job of parsing

The parsing is done in `parsing.py`. It is your job to implement the `parse` function.
A lot of the gritty work of counting parentheses and such has been done for you, but you must stitch everything together.

Have a look at the provided functions in the module, and start working. Run the following command until all tests pass.

    nosetests tests/test_1_parsing.py --stop

    nosetests tests/test_1_parsing_quotes.py --stop