"""This module contains functions and classes for handling numeric objects in pseudocode."""

__author__ = "Patryk Niedźwiedziński"

from pseudo.type.base import Value


def is_digit(c) -> bool:
    """Checks if given char is a digit."""
    try:
        return ord(c) >= 48 and ord(c) <= 57
    except TypeError:
        return False


class Int(Value):
    """Int value node."""

    def __init__(self, value):
        self.value = int(value)

    def __eq__(self, other):
        return self.value == other.value

    def __repr__(self):
        return f"Int({repr(self.value)})"
