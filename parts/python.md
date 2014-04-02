## Python Cheat Sheet

This is not an introduction to Python. 
For that, see the [Python tutorial](https://docs.python.org/2/tutorial/) or the [Python module index](https://docs.python.org/3/py-modindex.html).
Instead, this lists some tips and pointers that will prove useful when working on your language.

### Lists

Lists will comprise our ASTs, so you'll need lists pretty early on. The [tutorial page on lists](https://docs.python.org/2/tutorial/datastructures.html#more-on-lists) should prove useful.

### Dictionaries

We'll be using [dictionaries](https://docs.python.org/2/library/stdtypes.html#typesmapping) when representing the program environments.

- Remember that dicts are mutable in Python. Use the [`copy`](https://docs.python.org/2/library/stdtypes.html#dict.copy) function when a copy is needed.
- To update a dictionary with values from another, use [`update`](https://docs.python.org/2/library/stdtypes.html#set.update).
- You will find yourself needing to make a dictionary from a list of keys and a list of values. To do so, combine the [`dict`](https://docs.python.org/2/library/functions.html#func-dict) and [`zip`](https://docs.python.org/2/library/functions.html#zip) functions like this:
    
    ```python
    >>> dict(zip(["foo", "bar"], [1, 2]))
    {'foo': 1, 'bar': 2}
    ```

Read more about dicts in the [documentation](https://docs.python.org/2/tutorial/datastructures.html#dictionaries).

### Strings

- Strings works in many ways like lists. Thus, you can substring using indices:

    ```python
    >>> "hello world"[6:]
    'world'
    ```

- Remove unwanted whitespace using [`str.strip()`](https://docs.python.org/2/library/stdtypes.html#str.strip).

- It is also useful to know about how to do [string interpolation](https://docs.python.org/2/library/stdtypes.html#string-formatting-operations) in Python.

    ```python
    >>> "Hey, %s language!" % "cool"
    'Hey, cool language!'
    >>> "%d bottles of %s on the wall" % (99, "beer")
    '99 bottles of beer on the wall'
    >>> "%(num)s bottles of %(what)s on the %(where)s, %(num)d bottles of %(what)s" \
    ...      % {"num": 99, "what": "beer", "where": "wall"}
    '99 bottles of beer on the wall, 99 bottles of beer'
    ```

### Classes

When defining a class, all methods take a special argument `self` as the first argument. The `__init__` method works as constructor for the class.

```python
class Knight:
    
    def __init__(self, sound):
        self.sound = sound
    
    def speak(self):
        print self.sound
```

You don't provide the `self` when creating instances or calling methods:

```python
>>> knight = Knight("ni")
>>> knight.speak()
ni
```

### Default argument values

One thing it is easy to be bitten by is the way Python handles default function argument values. These are members of the function itself, and not "reset" every time the function is called.

```python
>>> def function(data=[]):
...     data.append(1)
...     return data
...
>>> function()
[1]
>>> function()
[1, 1]
>>> function()
[1, 1, 1]
```

Beware this when you implement the `Environment` class.
