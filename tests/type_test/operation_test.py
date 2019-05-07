"""This module contains tests for pseudo.type.operation"""

import pytest

from pseudo.stream import Stream
from pseudo.type.operation import is_operator, read_operator, Operator
from pseudo.type import Int, String


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


@pytest.mark.timeout(2)
def test_type_errors(runtime):
    try:
        Operator("-").eval(Int(1), String("test"), runtime)
    except SystemExit:
        pass
    else:
        raise AssertionError


@pytest.mark.timeout(2)
def test_operation_result(runtime, test):

    test(Operator("+").eval(Int(1), Int(2), runtime), 3)

    test(Operator("-").eval(Int(1), Int(2), runtime), -1)

    test(Operator("*").eval(Int(2), Int(2), runtime), 4)

    test(Operator("/").eval(Int(3), Int(2), runtime), 1.5)

    test(Operator("div").eval(Int(3), Int(2), runtime), 1)

    test(Operator("mod").eval(Int(5), Int(2), runtime), 1)

