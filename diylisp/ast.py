# -*- coding: utf-8 -*-

from .types import Closure, String

"""
This module contains a few simple helper functions for
checking the type of ASTs.
"""


def is_symbol(x):
    return isinstance(x, str)

def is_string(x):
    return isinstance(x, String)

def is_list(x):
    return isinstance(x, list)


def is_boolean(x):
    return isinstance(x, bool)


def is_integer(x):
    return isinstance(x, int)


def is_closure(x):
    return isinstance(x, Closure)


def is_atom(x):
    return (is_symbol(x) or
        is_integer(x) or
        is_string(x)
        is_boolean(x) or
        is_closure(x))
