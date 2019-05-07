"""This module contains all about variables in pseudocode."""

__author__ = "Patryk Niedźwiedziński"

from pseudo.type.base import Value, ASTNode
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
        return r.get(self.key(r))

    def key(self, r):
        postfix = ""
        for i in self.indices:
            postfix += f"[{str(i.eval(r))}]"
        return self.value + postfix

    def __repr__(self):
        return f'Variable("{self.value}")'

    def __str__(self):
        return self.__repr__()


class Increment(ASTNode):
    """
    Representing incrementation of iterator.
    
    Attributes:
        - key: str, Key of iterator.
        - line: str, Representation of operation in pseudocode.
    """

    def __init__(self, key: str, line: str = ""):
        self.key = key
        self.line = line

    def __eq__(self, other):
        try:
            return self.__dict__ == other.__dict__
        except AttributeError:
            return False

    def eval(self, r):
        r.var[self.key].incr()


class Assignment(ASTNode):
    """
    Node for representing assignments.

    Attributes:
        - target: Target variable.
        - value: Value to assign.
    """

    def __init__(
        self, target: Variable, value: Value, object_class=MemoryObject, line: str = ""
    ):
        self.target = target
        self.value = value
        self.object_class = object_class
        self.line = line

    def eval(self, r):
        r.save(self.target.key(r), self.value, object_class=self.object_class)

    def __eq__(self, other):
        try:
            return self.__dict__ == other.__dict__
        except AttributeError:
            return False

    def __repr__(self):
        return f"Assignment({self.target}, {self.value})"

    def __str__(self):
        return self.__repr__()
