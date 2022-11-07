# -*- coding: utf-8 -*-

"""
This module holds some types we'll have use for along the way.

It's your job to implement the Closure and Environment types.
The DiyLangError class you can have for free :)
"""


class DiyLangError(Exception):
    """General DIY Lang error class."""
    pass


class Closure(object):

    def __init__(self, env, params, body):
        self.env = env
        self.params = params
        self.body = body

    def __repr__(self):
        return "<closure/%d>" % len(self.params)


class Environment(object):

    def __init__(self, variables=None):
        self.bindings = variables if variables else {}

    def lookup(self, symbol):
        if symbol in self.bindings:
            return self.bindings[symbol]
        raise DiyLangError(f'variable "{symbol}" isn\'t defined')

    def extend(self, variables):
        env = Environment()
        for k, v in self.bindings.items():
            env.bindings[k] = v
        for k, v in variables.items():
            env.bindings[k] = v
        return env

    def set(self, symbol, value):
        if symbol in self.bindings:
            raise DiyLangError(f'variable "{symbol}" already defined')
        self.bindings[symbol] = value

    def update(self, symbol, value):
        self.bindings[symbol] = value

class String(object):

    """
    Simple data object for representing DIY Lang strings.

    Ignore this until you start working on part 8.
    """

    def __init__(self, val=""):
        self.val = val

    def __str__(self):
        return '"{}"'.format(self.val)

    def __eq__(self, other):
        return isinstance(other, String) and other.val == self.val

    def len(self):
        return len(self.val)

    def head(self):
        if len(self.val) == 0:
            raise DiyLangError('Empty string does not have head')
        return String(self.val[0])

    def tail(self):
        if len(self.val) == 0:
            raise DiyLangError('Empty string does not have tail')
        return String(self.val[1:])

    def cons(self, other):
        return String(self.val+other.val)
