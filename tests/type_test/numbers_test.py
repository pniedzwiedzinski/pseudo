"""This module contains test for `pseudo.type.numbers`"""

__author__ = "Patryk Niedźwiedziński"

import pytest
from pseudo.type.numbers import is_digit, read_number
from pseudo.stream import Stream


@pytest.mark.timeout(2)
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


@pytest.mark.timeout(2)
def test_read_number(lexer):
    """Checks read_number"""
    lexer.i = Stream("123")
    if 123 != read_number(lexer).value:
        raise AssertionError
    lexer.i = Stream("abc")
    if read_number(lexer) is not None:
        raise AssertionError

