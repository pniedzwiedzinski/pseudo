"""
This module contains classes for types in AST.
"""

__author__ = u"Patryk Niedźwiedziński"

class Value():
    """
    Node containing a value.

    Attributes:
        value: Value of instance.
    """
    def __init__(self, value):
        self.value = value

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


class Operator(Value):
    """Operator value node."""
    #TODO
    def __repr__(self):
        return f"Operator(\"{self.value}\")"


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

    def __repr__(self):
        return f"Expression(\"{self.value}\", args={self.args})"

    def __str__(self):
        return self.__repr__()


class EOL():
    """Representation of newline."""
    def __init__(self):
        pass

    def __repr__(self):
        return f"EOL()"

    def __str__(self):
        return "EOL"