import pytest

from pseudo.stream import Stream
from pseudo.type import Int
from pseudo.type.operation import Operation, Operator
from pseudo.type.variable import Assignment, Variable


@pytest.mark.timeout(2)
def test_assignment(runtime, lexer, test):
    lexer.i = Stream("a := 1")
    i = lexer.read_next()

    test(i, Assignment(Variable("a"), Int(1), line="a := 1"))
    runtime.eval(i)

    lexer.i = Stream("b := 2-1")
    i = lexer.read_next()

    test(
        i,
        Assignment(
            Variable("b"),
            Operation(Operator("-"), Int(2), Int(1), "b := 2-1"),
            line="b := 2-1",
        ),
    )
    runtime.eval(i)
