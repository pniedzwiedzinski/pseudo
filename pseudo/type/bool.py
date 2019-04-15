"""This module contains everything about bool in pseudocode."""

__author__ = "Patryk Niedźwiedziński"

from pseudo.type.base import Value


class Bool(Value):
    """Bool value node."""

    def __str__(self):
        if self.value:
            return "prawda"
        return "fałsz"

    def __repr__(self):
        return f"Bool({self.value})"


def read_bool(keyword: str) -> Bool:
    """Parse bool str to Bool object."""
    if keyword == "prawda":
        return Bool(1)
    if keyword == "fałsz":
        return Bool(0)
