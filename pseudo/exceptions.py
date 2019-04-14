"""This module contains exceptions that may occur during parsing pseudocode."""

__author__ = "Patryk Niedźwiedziński"


class IndentationBlockEnd(Exception):
    """This exception occurs when indentation block ends."""


class Comment(Exception):
    """This exception is raised when `#` is seen."""
