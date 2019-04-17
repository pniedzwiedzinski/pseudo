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

    def eval(self):
        if self.value == "pisz":
            a = self.args.eval()
            if a == "\\n":
                print("")
            else:
                print(a, end="")
        elif self.value == "czytaj":
            inp = input(self.args.value + ": ")
            try:
                inp = int(inp)
                inp = Int(inp)
            except ValueError:
                inp = String(inp)
            x = Assignment(self.args, inp)
            x.eval()
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


class Loop:
    """
    Node for representing looped actions.

    Attributes:
        - condition: Condition to check if loop should be executed.
        - expressions: List of expressions to execute if condition is positive.
    """

    def __init__(self, condition, expressions):
        self.condition = condition
        self.expressions = expressions

    def eval(self):
        while self.condition.eval():
            for e in self.expressions:
                e.eval()

    def __repr__(self):
        return f"Loop({self.condition}, {self.expressions})"

