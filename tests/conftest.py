import pytest
import pseudo


@pytest.fixture
def lexer():
    """Returns lexer object."""
    lex = pseudo.lexer.Lexer("")
    return lex
