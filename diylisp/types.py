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
        self.variables = variables if variables else {}

    def lookup(self, symbol):
        try:
    	    return self.variables[symbol]
        except KeyError:
            raise LispError("Undefined symbol: %s" % symbol)

    def extend(self, variables):
        new_variables = {}
        for key in self.variables:
            new_variables[key] = self.variables[key]
        for key in variables:
            new_variables[key] = variables[key]

        return Environment(new_variables)

    def set(self, symbol, value):
        try:
            dummy = self.variables[symbol]
        except KeyError:
            self.variables[symbol] = value
            return

	raise LispError("Symbol %s is already defined" % symbol)

    def __str__(self):
        env_string = ""
        for key in self.variables:
            env_string += key + ": " + self.variables[key] + "\n"
        return env_string
