## DIY Lisp 

> batteries included, some assembly required

In this tutorial/workshop we'll be implementing our own little language, more or less from scratch. 

By the end of the tutorial you will be the proud author of a programming language, and will hopefully better understand how programming languages work  on a fundamental level.

### What we will be making

We will make a relatively simple, but neat language. We aim for the following features:

- A handful of datatypes (integers, booleans and symbols)
- Variables
- First class functions with lexical scoping
- That nice homemade quality feeling

We will *not* have:

- A proper type system
- Error handling
- Good performance
- And much, much more

The language should be able to interpret the following code by the time we are done:

```lisp
(define fact 
    ;; Factorial function
    (lambda (n) 
        (if (eq n 0) 
            1 ; Factorial of 0 is 1
            (* n (fact (- n 1))))))

;; When parsing the file, the last statement is returned
(fact 5)
```

The syntax is that of the languages in the Lisp family. If you find the example unfamiliar, you might want to have a look at [a more detailed description of the language](parts/language.md).

### Prerequisites

Before we get started, make sure you have installed [Python](http://www.python.org/) and [Pip](https://pypi.python.org/pypi/pip). 
*(It should now work with Python 3. If you have any problem with it, please [fill an issue](https://github.com/kvalle/diy-lisp/issues).)*

Then install `nose`, the Python test framework we'll be using.

```bash
pip install nose
```

*Optional: If you are familiar with [virtualenv](http://www.virtualenv.org/en/latest/) you might want to do this in a separate pyenv.*

Finally, clone this repo, and you're ready to go!

```bash
git clone https://github.com/kvalle/diy-lisp.git
```

> Also, if you're unfamiliar with Python, you might want to have a look at the basics in the [Python tutorial](https://docs.python.org/2/tutorial/index.html) before we get going. There is also the small [Python cheat sheet](parts/python.md) to help you along.

### A few tips

Take the time to consider the following points before we get going:

- **Keep things simple**
  
  	Don't make things more complicated than they need to be. The tests should hopefully guide you every step of the way.

- **Read the test descriptions**

  	Each test has a small text describing what you are going to implement and why. Reading these should make things easier, and you might end up learning more.

- **Use the provided functions**

  	Some of the more boring details are already taken care of. Take the time to look at the functions provided in `parser.py`, and the various imports in files where you need to do some work.

- **The Python cheat sheet in `python.md`**

  	Unless you're fluent in Python, there should be some helpful pointers in the [Python cheat sheet](https://github.com/kvalle/diy-lisp/blob/master/parts/python.md).

- **Description of your language**

  	Unfamiliar with Lisp? Read a description of the language you are going to make in [language.md](https://github.com/kvalle/diy-lisp/blob/master/parts/language.md).

### Get started!

The workshop is split up into eight parts. Each consist of an introduction, and a bunch of unit tests which it is your task to make run. When all the tests run, you'll have implemented that part of the language.

Have fun!

- [Part 1: parsing](parts/1.md)
- [Part 2: evaluating simple expressions](parts/2.md)
- [Part 3: evaluating complex expressions](parts/3.md)
- [Part 4: working with variables](parts/4.md)
- [Part 5: functions](parts/5.md)
- [Part 6: working with lists](parts/6.md)
- [Part 7: using your language](parts/7.md)
- [Part 8: final touches](parts/8.md)
