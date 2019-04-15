"""This module contains all about variables in pseudocode."""

__author__ = "Patryk Niedźwiedziński"

from pseudo.type.base import Value


VAR = {}


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

    def setter(self, value: Value):
        if not self.indices:
            VAR[self.value] = value.eval()
            return None

        if self.value not in VAR:
            VAR[self.value] = {}
        v = VAR[self.value]

        for key in self.indices[:-1]:
            try:
                v = v[key.eval()]
            except KeyError:
                v[key.eval()] = {}
                v = v[key.eval()]
        v[self.indices[-1].eval()] = value.eval()

    def getter(self):
        try:
            var = VAR[self.value]
            for key in self.indices:
                var = var.__getitem__(key.eval())
            return var
        except KeyError:
            return "nil"

    def eval(self):
        return self.getter()

    def __repr__(self):
        return f'Variable("{self.value}", {self.indices})'

    def __str__(self):
        return self.__repr__()


class Assignment:
    """
    Node for representing assignments.

    Attributes:
        - target: Target variable.
        - value: Value to assign.
    """

    def __init__(self, target: Variable, value: Value):
        self.target = target
        self.value = value

    def eval(self):
        self.target.setter(self.value)

    def __repr__(self):
        return f"Assignment({self.target}, {self.value})"

    def __str__(self):
        return self.__repr__()
