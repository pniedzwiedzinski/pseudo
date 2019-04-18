"""This module contains functions and classes for handling numeric objects in pseudocode."""

__author__ = "Patryk Niedźwiedziński"

from pseudo.type.base import Value


class Int(Value):
    """Int value node."""

    def __init__(self, value):
        self.value = int(value)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"Int({repr(self.value)})"


def is_digit(c) -> bool:
    """Checks if given char is a digit."""
    try:
        return ord(c) >= 48 and ord(c) <= 57
    except TypeError:
        return False


def read_number(lexer) -> Int:
    """Read a number from the stream."""
    number = lexer.read(is_digit)
    try:
        int(number)
    except ValueError:
        return None
    return Int(number)

