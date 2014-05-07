## The Language

The syntax of our little language is Lisp-inspired. This is mainly to make it easy to write the parser.

We will handle two types of expressions: **atoms** and **lists**. 

- Atoms can be numbers (`42`), booleans(`#t` and `#f`) or symbols (`foobar`).
- Lists consists of a series of zero or more expressions (other atoms or lists) separated by spaces and enclosed by parentheses.

### Evaluation rules

- Numbers and booleans evaluate to themselves.
- Symbols are treated as variable references. When evaluated, their values are looked up in the environment.
- Lists are treated as function calls (or calls to the special forms built into the language).
- Anything in between semicolons (`;`) and the end of a line is considered a comment and ignored.

### Special Forms

The language will have a set of "special forms". These are the construct built into the language. If a list expression is evaluated, and the first element is one of a number of defined symbols, the special form is executed: 

Here is a brief explanation of each form:

- `quote` takes one argument which is returned without it being evaluated.
- `atom` is a predicate indicating whether or not it's one argument is an atom.
- `eq` returns true (`#t`) if both its arguments are the same atom.
- `+`, `-`, `*`, `/`, `mod` and `>` all take two arguments, and does exactly what you would expect. (Note that since we have no floating point numbers, the `/` represent integer division.)
- `if` is the conditional, taking three arguments. It's return value is the result of evaluating the second or third argument, depending on the value of the first one.
- `define` is used to define new variables in the environment.
- `lambda` creates function closures.
- `cons` is used to construct lists from a head (element) and the tail (list).
- `head` returns the first element of a list.
- `tail` returns all but the first element of a list.

### Function calls

If a list is evaluated, and the first element is something other than one of the special forms, it is expected to be a function closure. Function closures are created using the `lambda` form. 

Here is a (rather silly) example showing how to define and use a function.

```lisp
(define my-function
    ;; This function returns 42, unless the argument 
    ;; actually is 42. In that case, we return 1000.
    (lambda (n) 
        (if (eq n 42) 
            1000
            42)))

(my-function 42) ;; => 1000
```

This might for some be the most "magic" part, and one that you hopefully will understand a lot better after implementing the language.
