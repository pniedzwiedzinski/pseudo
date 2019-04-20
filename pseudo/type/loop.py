"""This module contains ASTNode for loop and iterator memory object."""

__author__ = "Patryk Niedźwiedziński"

from pseudo.runtime import MemoryObject
from pseudo.type.base import Value


class Iterator(MemoryObject):
    """
    This class is a representation of iterator in memory.
    """

    def __init__(self, value: int, line: str = ""):
        MemoryObject.__init__(self, value, const=True, line=line)

    def setter(self, _, r):
        r.throw("Cannot set value of iterator", self.line)

    def incr(self, key):
        self.value += 1


class Loop:
    """
    Node for representing looped actions.

    Attributes:
        - condition: Condition to check if loop should be executed.
        - expressions: List of expressions to execute if condition is positive.
    """

    def __init__(self, condition, expressions, iterator=None, line=""):
        self.condition = condition
        self.expressions = expressions
        self.iterator = iterator
        self.line = line

    def eval(self, r):
        while self.condition.eval(r):
            for e in self.expressions:
                e.eval(r)
        if self.iterator is not None:
            r.delete(self.iterator.value)

    def __repr__(self):
        return f"Loop({self.condition}, {self.expressions})"
