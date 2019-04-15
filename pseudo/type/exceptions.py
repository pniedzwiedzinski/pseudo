"""This module contains exceptions that may occur during run time."""

__author__ = "Patryk Niedźwiedziński"


class NoSetter(Exception):
    """This exception occurs when variable has no setter, but it was called."""
