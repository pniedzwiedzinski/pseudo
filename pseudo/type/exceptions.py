"""This module contains exceptions that may occur during run time."""

__author__ = "Patryk Niedźwiedziński"


class NoSetter(Exception):
    """This exception occurs when variable has no setter, but it was called."""


class ReturnCall(Exception):
    """
    This exception is raised when `return` keyword is called.
    """

    def __init__(self, return_value):
        self.return_value = return_value
