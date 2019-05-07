import pytest
import pseudo
from pseudo.runtime import RunTime
from pseudo.scope import Scope


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
def scope():
    main = Scope()
    s = Scope(main)
    return s


@pytest.fixture
def test():
    def _test(a, b):
        if a != b:
            print(a)
            raise AssertionError

    return _test

