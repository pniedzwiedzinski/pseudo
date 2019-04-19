"""This module contains all about variables in pseudocode."""

__author__ = "Patryk Niedźwiedziński"

from pseudo.type.base import Value
from pseudo.runtime import MemoryObject


class Variable(Value):
    """
    Node for representing variables.

    Attributes:
        - value: Name of the variable.
        - indices: List of indices.
    """

    def __init__(self, value, indices=[]):
        self.value = value
        self.indices = indices

    def eval(self, r):
        return r.get(self.value)

    def __repr__(self):
        return f'Variable("{self.value}", {self.indices})'

    def __str__(self):
        return self.__repr__()


class Increment:
    """Representing incrementation of iterator."""
    def __init__(self, key: str):
        self.key = key

    def eval(self, r):
        r.var[self.key].incr(self.key)


class Assignment:
    """
    Node for representing assignments.

    Attributes:
        - target: Target variable.
        - value: Value to assign.
    """

    def __init__(self, target: Variable, value: Value, object_class = MemoryObject):
        self.target = target
        self.value = value
        self.object_class = object_class

    def eval(self, r):
        r.save(self.target.value, self.value, object_class=self.object_class)

    def __repr__(self):
        return f"Assignment({self.target}, {self.value})"

    def __str__(self):
        return self.__repr__()
