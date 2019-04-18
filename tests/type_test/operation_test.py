"""This module contains tests for pseudo.type.operation"""

import pytest

from pseudo.stream import Stream
from pseudo.type.operation import is_operator, read_operator, Operator


@pytest.mark.timeout(2)
def test_is_operator(test):
    """Checks is_operator"""

    test(is_operator("*"), True)
    test(is_operator("div"), True)
    test(is_operator(":="), False)
    test(is_operator("pisz"), False)


@pytest.mark.timeout(2)
def test_read_operator(test):
    """Checks read_operator"""

    test(read_operator(Stream("*")), Operator("*"))

    # try:
    #     read_operator(Stream("sadscda"))
    # except SystemExit:
    #     pass
    # else:
    #     raise AssertionError
