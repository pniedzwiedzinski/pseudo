import pytest
import pseudo
from pseudo.runtime import RunTime


@pytest.fixture
def lexer():
    """Returns lexer object."""
    lex = pseudo.lexer.Lexer("")
    return lex


@pytest.fixture
def runtime():
    r = RunTime()
    return r


@pytest.fixture
def test():
    def _test(a, b):
        if a != b:
            print(a.__dict__)
            print(b.__dict__)
            raise AssertionError

    return _test

