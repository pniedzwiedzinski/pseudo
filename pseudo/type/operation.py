"""This module contains classes for representing operations in AST."""

__author__ = "Patryk Niedźwiedziński"


from pseudo.type.base import Value
from pseudo.type.bool import Bool


GROUP_1 = {"*", "div", "mod"}
GROUP_2 = {"-", "+"}

OPERATORS = {"+", "-", "*", ":", "<", ">", "=", "!"}
OPERATOR_KEYWORDS = {"div", "mod"}


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

        # Then operation is boolean
        return Bool.eval_operation(self.value, left, right)

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


def is_operator(c) -> bool:
    """Checks if given char is an allowed operator."""
    try:
        return c in OPERATORS or c in OPERATOR_KEYWORDS
    except TypeError:
        return False


def read_operator(stream):
    """
    Return operator from input stream.
    
    Args:
        - stream: Input stream
    """
    c = stream.next()
    is_assignment = (c == ":" and stream.peek() == "=") or (
        c == "<" and stream.peek() == "-"
    )

    if is_assignment:  # :=, <-
        stream.next()
        return ":="

    is_comparison = stream.peek() == "=" and (c == "!" or c in "<>")
    if is_comparison:  # !=, <= , >=
        return Operator(c + stream.next())

    return Operator(c)


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
