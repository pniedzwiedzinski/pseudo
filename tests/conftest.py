import pytest
import pseudo


@pytest.fixture
def lexer():
    """Returns lexer object."""
    lex = pseudo.lexer.Lexer("")
    return lex


@pytest.fixture
def test():
    def _test(a, b):
        if a != b:
            print(a)
            raise AssertionError

    return _test

