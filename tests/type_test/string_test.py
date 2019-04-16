"""This module contains tests for pseudo.type.string"""

import pytest
from pseudo.type.string import read_string
from pseudo.stream import Stream


@pytest.mark.timeout(2)
def test_read_string(lexer, test):
    """Checks Lexer.read_string"""
    lexer.i = Stream('"abc"')
    test(read_string(lexer).value, "abc")

    lexer.i = Stream('"abc')
    try:
        print(read_string(lexer))
    except SystemExit:
        pass
    else:
        raise AssertionError
