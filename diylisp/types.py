# -*- coding: utf-8 -*-

"""
This module holds some types we'll have use for along the way.

It's your job to implement the Closure and Environment types.
The LispError class you can have for free :)
"""

class LispError(Exception): 
    """General lisp error class."""
    pass

class Closure:
    
    def __init__(self, env, params, body):
        self.env = env
        self.params = params
        self.body = body

    def __str__(self):
        return "<closure/%d>" % len(self.params)

class Environment:

    def __init__(self, variables=None):
        self.bindings = variables if variables else {}

    def lookup(self, symbol):
        if symbol in self.bindings:
            return self.bindings[symbol]
        else:
            raise LispError("Variable '%s' is undefined" % symbol)

    def extend(self, variables):
        new_bindings = self.bindings.copy()
        new_bindings.update(variables)
        return Environment(new_bindings)

    def set(self, symbol, value):
        if symbol in self.bindings:
            raise LispError("Variable '%s' is already defined." % symbol)
        self.bindings[symbol] = value
