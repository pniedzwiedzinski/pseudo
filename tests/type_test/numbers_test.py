"""This module contains test for `pseudo.type.numbers`"""

__author__ = "Patryk Niedźwiedziński"

from pseudo.type.numbers import is_digit


def test_is_digit():
    """Check is_digit"""
    if not (
        is_digit("1") is True and is_digit("a") is False and is_digit('"') is False
    ):
        raise AssertionError
