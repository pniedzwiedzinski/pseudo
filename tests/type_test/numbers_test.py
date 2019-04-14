"""This module contains test for `pseudo.type.numbers`"""

__author__ = "Patryk Niedźwiedziński"

from pseudo.type.numbers import is_digit


def test_is_digit():
    """Check is_digit"""
    if is_digit("1") is False:
        print(is_digit("1"))
        raise AssertionError
    if is_digit("a") is True:
        print(is_digit("a"))
        raise AssertionError
    if is_digit('"') is True:
        print(is_digit('"'))
        raise AssertionError
