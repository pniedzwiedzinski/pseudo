"""This module contains everything about strings."""

__author__ = "Patryk Niedźwiedziński"

from pseudo.type.base import Value


class String(Value):
    """String value node."""

    def __repr__(self):
        return f'String("{self.value}")'


def read_string(lexer) -> String:
    """Read a string from the stream."""
    lexer.i.next()
    string = lexer.read(lambda c: c != '"')
    try:
        string_end = lexer.i.next() == '"'
    except IndexError:
        string_end = False
    if not string_end:
        lexer.i.throw(f"Could not parse string")
    return String(string)

