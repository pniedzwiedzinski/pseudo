"""This module contains base class for all objects representing value in AST"""

__author__ = "Patryk Niedźwiedziński"


class Value:
    """
    Node containing a value.

    Attributes:
        - value: Value of instance.
    """

    def __init__(self, value):
        self.value = value

    def eval(self):
        return self.value

    def __eq__(self, other):
        try:
            return self.value == other.value
        except AttributeError:
            return False

    def __repr__(self):
        return f"Value({repr(self.value)})"

    def __str__(self):
        return str(self.value)


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
