"""This module contains tests from pseudo.type.variable"""

import pytest
from pseudo.type.numbers import Int
from pseudo.type.variable import Variable, VAR


@pytest.mark.timeout(2)
def test_getter(test):
    """Checks Variable.getter"""
    VAR["a"] = 1

    v = Variable("a").getter()

    test(v, 1)

    VAR["b"] = {}
    VAR["b"][1] = {}
    VAR["b"][1][5] = 3

    v = Variable("b", indices=[Int(1), Int(5)]).getter()

    test(v, 3)


@pytest.mark.timeout(2)
def test_setter(test):
    """Checks Variable.setter"""
    Variable("a").setter(Int(1))

    test(VAR["a"], 1)

    Variable("b", indices=[Int(1), Int(5)]).setter(Int(3))

    test(VAR["b"][1][5], 3)

