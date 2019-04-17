"""
This module contains classes for types in AST.
"""


__author__ = "Patryk Niedźwiedziński"

from pseudo.type.numbers import Int
from pseudo.type.string import String
from pseudo.type.bool import Bool
from pseudo.type.variable import Variable, Assignment
from pseudo.type.base import Value, EOL


GROUP_1 = {"*", "div", "mod"}
GROUP_2 = {"-", "+"}


class Operator(Value):
    """Opartor class for representing mathematical operator."""

    def eval(self, left: Value, right: Value):
        if self.value == "+":
            return left.eval() + right.eval()
        if self.value == "-":
            return left.eval() - right.eval()
        if self.value == "*":
            return left.eval() * right.eval()
        if self.value == "div":
            return left.eval() // right.eval()
        if self.value == "mod":
            return left.eval() % right.eval()

        if self.value == "=":
            if left.eval() == right.eval():
                return 1
            return 0
        if self.value == "!=":
            if left.eval() != right.eval():
                return 1
            return 0
        if self.value == ">":
            if left.eval() > right.eval():
                return 1
            return 0
        if self.value == "<":
            if left.eval() < right.eval():
                return 1
            return 0
        if self.value == "<=":
            if left.eval() <= right.eval():
                return 1
            return 0
        if self.value == ">=":
            if left.eval() >= right.eval():
                return 1
            return 0

    def __lt__(self, o):
        if self.value in GROUP_2:
            if o.value in GROUP_1:
                return True
        return False

    def __gt__(self, o):
        if self.value in GROUP_1:
            return True
        if self == o:
            return True
        return False

    def __eq__(self, o):
        try:
            if self.value == o.value:
                return True
            if self.value in GROUP_1 and o.value in GROUP_1:
                return True
            if self.value in GROUP_2 and o.value in GROUP_2:
                return True
            return False
        except AttributeError:
            return False

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"Operator({repr(self.value)})"


class Operation:
    """Operation node."""

    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

    def eval(self):
        return self.operator.eval(self.left, self.right)

    def __eq__(self, other):
        try:
            return self.__dict__ == other.__dict__
        except AttributeError:
            return False

    def __repr__(self):
        return f"Operation({self.operator}, {self.left}, {self.right})"


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

