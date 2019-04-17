"""This module contains tests for pseudo.type.conditional"""

import pytest

from pseudo.stream import Stream
from pseudo.type import Statement
from pseudo.type.operation import Operation, Operator
from pseudo.type.base import EOL
from pseudo.type.bool import Bool
from pseudo.type.numbers import Int
from pseudo.type.conditional import Condition, read_if


@pytest.mark.timeout(2)
def test_read_if(lexer, test):
    """Checks Lexer.read_if"""
    lexer.i = Stream(
        """jeżeli prawda to
    pisz 4
wpp
    pisz 3"""
    )
    lexer.i.col = 7

    test(
        read_if(lexer),
        Condition(
            Bool(1),
            [Statement("pisz", args=Int(4)), EOL()],
            [Statement("pisz", args=Int(3)), EOL()],
        ),
    )

    lexer.i = Stream(
        """jeżeli 2 > 3+2 to
    4"""
    )
    lexer.i.col = 7

    test(
        read_if(lexer),
        Condition(
            Operation(Operator(">"), Int(2), Operation(Operator("+"), Int(3), Int(2))),
            [Int(4), EOL()],
            None,
        ),
    )
