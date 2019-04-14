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
