"""This module contains tests for pseudo.type.string"""

import pytest
from pseudo.type.string import read_string
from pseudo.stream import Stream


@pytest.mark.timeout(2)
def test_read_string(lexer):
    """Checks Lexer.read_string"""
    lexer.i = Stream('"abc"')
    if "abc" != read_string(lexer).value:
        raise AssertionError
