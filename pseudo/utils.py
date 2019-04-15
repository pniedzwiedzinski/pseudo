"""This module contains functions to handle custom operations."""

__author__ = "Patryk Niedźwiedziński"


def append(l: list, obj: object) -> list:
    """Extend or append to list"""
    if isinstance(obj, list):
        l.extend(obj)
    else:
        l.append(obj)
    return l
