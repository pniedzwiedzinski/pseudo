"""This module contains test for `pseudo.type.loop`"""

import pytest

from pseudo import compile
from pseudo.runtime import RunTime
from pseudo.stream import Stream
from pseudo.type import Statement, EOL
from pseudo.type.numbers import Int
from pseudo.type.bool import Bool
from pseudo.type.variable import Assignment, Variable, Increment
from pseudo.type.operation import Operation, Operator
from pseudo.type.loop import Loop, read_for, read_while, Iterator

pdc = """
dla i:=1,...,5 wykonuj
    pisz i
    i := i+1
"""


def test_unsettable_iterator():
    instructions = compile(pdc)

    r = RunTime()

    try:
        for i in instructions:
            i.eval(r)
    except SystemExit:
        pass
    else:
        raise AssertionError


@pytest.mark.timeout(2)
def test_read_for(lexer, runtime, test, monkeypatch):
    """Checks read_for"""
    lexer.i = Stream(
        """dla i:=1,...,5 wykonuj
    pisz i"""
    )
    lexer.i.col = 4

    T = []

    def mock_print(x, *args, **kwargs):
        T.append(x)

    monkeypatch.setattr("builtins.print", mock_print)

    runtime.run(read_for(lexer))

    test(T, [1, 2, 3, 4, 5])

    # Test lack of indentation block
    lexer.i = Stream("dla 1 := 1,...,5 wykonuj")
    lexer.i.col = 4

    try:
        runtime.run(read_for(lexer))
    except SystemExit:
        pass
    else:
        raise AssertionError

    lexer.i = Stream(
        """dla a := 1,...,5 wykonuj


"""
    )
    lexer.i.col = 4

    try:
        runtime.run(read_for(lexer))
    except SystemExit:
        pass
    else:
        raise AssertionError


@pytest.mark.timeout(2)
def test_read_while(lexer, test):
    lexer.i = Stream(
        """dopóki prawda wykonuj
    pisz a"""
    )
    lexer.i.col = 7

    test(
        read_while(lexer),
        Loop(
            Bool(1),
            [Statement("pisz", Variable("a")), EOL()],
            line="dopóki prawda wykonuj",
        ),
    )
