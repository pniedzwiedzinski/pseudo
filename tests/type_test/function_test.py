import pytest

from pseudo import compile
from pseudo.type import Int, Statement, EOL
from pseudo.type.function import Call, FunctionDefinition, read_function
from pseudo.stream import Stream


@pytest.mark.timeout(2)
def test_call(lexer, test):
    lexer.i = Stream("call()")
    i = lexer.read_next()

    test(i, Call("call", line="call()"))

    lexer.i = Stream("call(1)")
    i = lexer.read_next()

    test(i, Call("call", args=[Int(1)], line="call(1)"))

    lexer.i = Stream("call(2-1)")
    i = lexer.read_next()

    test(i, Call("call", args=[Int(1)], line="call(2-1)"))


@pytest.mark.timeout(2)
def test_read_function(lexer, test):
    lexer.i = Stream(
        """funkcja a()
    pisz 1"""
    )

    i = lexer.read_next()

    test(
        i,
        FunctionDefinition("a", [], [Statement("pisz", Int(1)), EOL()], "funkcja a()"),
    )


@pytest.mark.timeout(2)
def test_return(runtime, test, monkeypatch):
    instructions = compile(
        """funkcja a(b)
    zwróć b
    
pisz a(2)"""
    )

    T = []

    def mock_print(x, *args, **kwargs):
        T.append(x)

    monkeypatch.setattr("builtins.print", mock_print)

    runtime.run(instructions)

    test(T, [2])

