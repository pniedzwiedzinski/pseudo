"""
This module contains classes for types in AST.
"""


__author__ = "Patryk Niedźwiedziński"

from pseudo.type.numbers import Int
from pseudo.type.string import String
from pseudo.type.bool import Bool
from pseudo.type.variable import Variable, Assignment
from pseudo.type.base import Value, EOL


class Statement:
    """
    Node for statement with arguments.

    Attributes:
        - value: Statement name.
        - args: Arguments of statement.
    """

    def __init__(self, value, args=None):
        self.value = value
        self.args = args

    def eval(self, r):
        if self.value == "pisz":
            r.stdout(self.args.eval(r))
        elif self.value == "czytaj":
            r.stdin(self.args.value)
        elif self.value == "koniec":
            exit()

    def __eq__(self, other):
        try:
            return self.value == other.value and self.args == other.args
        except AttributeError:
            return False

    def __repr__(self):
        return f'Statement("{self.value}", args={self.args})'

    def __str__(self):
        return self.__repr__()

