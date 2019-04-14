"""
This module contains classes for types in AST.
"""


__author__ = "Patryk Niedźwiedziński"

from pseudo.type.numbers import Int
from pseudo.type.base import Value

VAR = {}

GROUP_1 = {"*", "div", "mod"}
GROUP_2 = {"-", "+"}


class String(Value):
    """String value node."""

    def __repr__(self):
        return f'String("{self.value}")'


class Bool(Value):
    """Bool value node."""

    def __str__(self):
        if self.value:
            return "prawda"
        return "fałsz"

    def __repr__(self):
        return f"Bool({self.value})"


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
        if self.value in GROUP_1 and o.value in GROUP_1:
            return True
        if self.value in GROUP_2 and o.value in GROUP_2:
            return True
        return False

    def __repr__(self):
        return self.value


class Operation:
    """Operation node."""

    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

    def eval(self):
        return self.operator.eval(self.left, self.right)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return f"({self.left}{self.operator}{self.right})"


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

    def eval(self):
        try:
            var = VAR[self.value]
            for key in self.indices:
                var = var.__getitem__(key.eval())
            return var
        except KeyError:
            return "nil"

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

    def __init__(self, target, value):
        self.target = target
        self.value = value

    def eval(self):
        try:
            v = VAR[self.target.value]
        except KeyError:
            VAR[self.target.value] = {}
            v = VAR[self.target.value]
        for key in self.target.indices[:-1]:
            try:
                v = v[key.eval()]
            except KeyError:
                v[key.eval()] = {}
                v = v[key.eval()]
        if len(self.target.indices) > 0:
            v[self.target.indices[-1].eval()] = self.value.eval()
        else:
            VAR[self.target.value] = self.value.eval()

    def __repr__(self):
        return f"Assignment({self.target}, {self.value})"

    def __str__(self):
        return self.__repr__()


class Condition:
    """
    Node for representing conditional expressions (if).

    Attributes:
        - condition: Condition to check
        - true: List to evaluate if condition is true
        - false: List to evaluate if condition is false (optional)
    """

    def __init__(self, condition, true, false=None):
        self.condition = condition
        self.true = true
        self.false = false

    def eval(self):
        b = self.condition.eval()
        if b and b != "nil":
            for x in self.true:
                x.eval()
        elif self.false is not None:
            for x in self.false:
                x.eval()

    def __eq__(self, other):
        if not isinstance(other, Condition):
            return False
        if self.condition != other.condition:
            return False
        if len(self.true) != len(other.true):
            return False
        if len(self.false) != len(other.false):
            return False
        for a, b in zip(self.true, other.true):
            if a != b:
                return False
        for a, b in zip(self.false, other.false):
            if a != b:
                return False
        return True

    def __repr__(self):
        return f"Condition({self.condition}, {self.true}, {self.false})"


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


class EOL:
    """Representation of newline."""

    def __init__(self):
        pass

    def eval(self):
        pass

    def __eq__(self, other):
        return isinstance(other, EOL)

    def __repr__(self):
        return f"EOL()"

    def __str__(self):
        return "EOL"
