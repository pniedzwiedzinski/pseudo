"""
This module contains classes for types in AST.
"""

VAR = {}

__author__ = u"Patryk Niedźwiedziński"

class Value():
    """
    Node containing a value.

    Attributes:
        value: Value of instance.
    """

    def __init__(self, value):
        self.value = value

    def eval(self):
        return self.value

    def __repr__(self):
        return f"Value({repr(self.value)})"

    def __str__(self):
        return str(self.value)


class Int(Value):
    """Int value node."""
    def __init__(self, value):
        self.value = int(value)

    def __repr__(self):
        return f"Int({repr(self.value)})"


class String(Value):
    """String value node."""
    def __repr__(self):
        return f"String(\"{self.value}\")"


class Bool(Value):
    """Bool value node."""
    def __repr__(self):
        return f"Bool({bool(self.value)})"


class Operation():
    """Operator value node."""
    def __init__(self, value, left, right):
        self.value = value
        self.left = left
        self.right = right

    def eval(self):
        if self.value == "+":
            return self.left.eval() + self.right.eval()
        if self.value == "-":
            return self.left.eval() - self.right.eval()

    def __repr__(self):
        return f"Operation({self.left}{self.value}{self.right})"


class Statement():
    """
    Node for statement with arguments.

    Attributes:
        value: Statement name.
        args: Arguments of statement.
    """

    def __init__(self, value, args=None):
        self.value = value
        self.args = args

    def eval(self):
        if self.value == "pisz":
            print(self.args.eval())
        elif self.value == "czytaj":
            x = Assignment(self.args, input(self.args.name + ": "))
        elif self.value == "koniec":
            exit(self.args.eval())

    def __repr__(self):
        return f"Statement(\"{self.value}\", args={self.args})"

    def __str__(self):
        return self.__repr__()


class Variable():
    """
    Node for representing variables.

    Attributes:
        name: Name of the variable.
    """

    def __init__(self, name):
        self.name = name

    def eval(self):
        return VAR[self.name]

    def __repr__(self):
        return f"Variable(\"{self.name}\")"

    def __str__(self):
        return self.__repr__()


class Assignment():
    """
    Node for representing assignments.

    Attributes:
        target: Target variable.
        value: Value to assign.
    """

    def __init__(self, target, value):
        self.target = target
        self.value = value

    def eval(self):
        VAR[self.target.name] = self.value.eval()

    def __repr__(self):
        return f"Assignment({self.target}, {self.value})"

    def __str__(self):
        return self.__repr__()


class EOL():
    """Representation of newline."""
    def __init__(self):
        pass

    def eval(self):
        pass

    def __repr__(self):
        return f"EOL()"

    def __str__(self):
        return "EOL"