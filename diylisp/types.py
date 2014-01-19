# -*- coding: utf-8 -*-

def is_symbol(x):
    return isinstance(x, str)

def is_list(x):
    return isinstance(x, list)

def is_boolean(x):
    return isinstance(x, bool)

def is_integer(x):
    return isinstance(x, int)

def is_lambda(x):
    return isinstance(x, Lambda)

def is_atom(x):
    return is_symbol(x) \
        or is_integer(x) \
        or is_boolean(x) \
        or is_lambda(x)

class Lambda:
    def __init__(self, params, body, env):
        self.params = params
        self.body = body
        self.env = env

    def __str__(self):
        return "<lambda/%d>" % len(self.params)

class Environment:
    def __init__(self, variables=None):
        self.bindings = variables if variables else {}

    def set(self, symbol, value):
        self.bindings[symbol] = value

    def extend(self, variables):
        new_bindings = self.bindings.copy()
        new_bindings.update(variables)
        print new_bindings
        return Environment(new_bindings)

    def lookup(self, symbol):
        print symbol
        print self.bindings
        if symbol in self.bindings:
            return self.bindings[symbol]
        else:
            raise LispError("Variable '%s' is undefined" % symbol)

class LispError(Exception): 
    pass

