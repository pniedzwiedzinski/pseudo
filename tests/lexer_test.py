"""This module contains unit tests for lexer module."""

import pytest
import pseudo

from pseudo.type.operation import Operation, Operator
from pseudo.type.loop import Loop
from pseudo.type import Int, Statement, Bool
from pseudo.type.variable import Variable, Assignment
from pseudo.stream import Stream, EOL, EndOfFile

__author__ = "Patryk Niedźwiedziński"


def compare_list(first: list, second: list) -> bool:
    """
    Compare two list if they are exact the same.

    Args:
        - first: list
        - second: list
    """

    if len(first) != len(second):
        return False

    return all([a == b for a, b in zip(first, second)])


@pytest.mark.timeout(2)
def test_is_keyword(lexer):
    """Check Lexer.is_keyword"""
    if lexer.is_keyword("pisz") is False:
        print(lexer.is_keyword("pisz"))
        raise AssertionError
    if lexer.is_keyword("oo") is True:
        print(lexer.is_keyword("oo"))
        raise AssertionError
    if lexer.is_keyword("koniec") is False:
        print(lexer.is_keyword("koniec"))
        raise AssertionError


@pytest.mark.timeout(2)
def test_is_keyword_end(lexer):
    """Checks Lexer.is_not_keyword_end"""
    if lexer.is_keyword_end("a") is True:
        print(lexer.is_keyword_end("a"))
        raise AssertionError
    if lexer.is_keyword_end("+") is False:
        print(lexer.is_keyword_end("+"))
        raise AssertionError
    if lexer.is_keyword_end("!") is False:
        print(lexer.is_keyword_end("!"))
        raise AssertionError


@pytest.mark.timeout(2)
def test_update_args(lexer):
    """Checks Lexer.update_args"""
    if lexer.update_args([Int(2), Operator("+"), Int(2)], 1) != [
        Operation(Operator("+"), Int(2), Int(2))
    ]:
        print(lexer.update_args([Int(2), Operator("+"), Int(2)], 1))
        raise AssertionError


@pytest.mark.timeout(2)
def test_read_keyword(lexer):
    """Checks Lexer.read_keyword"""
    lexer.i = Stream("pisz x")
    if "pisz" != lexer.read_keyword():
        raise AssertionError


@pytest.mark.timeout(2)
def test_read_condition(lexer):
    """Checks Lexer.read_condition"""
    lexer.i = Stream("jeżeli prawda to")
    lexer.i.col = 7

    if lexer.read_condition("jeżeli") != Bool(1):
        raise AssertionError

    lexer.i = Stream("dopóki prawda wykonuj")
    lexer.i.col = 7

    if lexer.read_condition("dopóki") != Bool(1):
        raise AssertionError


@pytest.mark.timeout(2)
def test_read_args(lexer, test):
    """Checks Lexer.read_args"""
    lexer.i = Stream("    12")
    lexer.i.col = 3
    if not compare_list(lexer.read_args(), [Int(12)]):
        raise AssertionError
    lexer.i = Stream("2+2*2")
    if not compare_list(
        lexer.read_args(), [Int(2), Operator("+"), Int(2), Operator("*"), Int(2)]
    ):
        raise AssertionError
    lexer.i = Stream("(2+2)*2")
    if not compare_list(
        lexer.read_args(),
        [
            Operation(Operator("+"), Int(2), Int(2), line="(2+2)*2"),
            Operator("*"),
            Int(2),
        ],
    ):
        raise AssertionError

    lexer.i = Stream("prawda")
    test(lexer.read_args(), [Bool(1)])


@pytest.mark.timeout(2)
def test_read_expression(lexer, runtime):
    """Checks Lexer.read_expression"""
    if (
        lexer.read_expression(
            [Int(2), Operator("+"), Int(2), Operator("*"), Int(2)]
        ).eval(runtime)
        != 6
    ):
        raise AssertionError

    try:
        lexer.read_expression([Int(2), Bool(1)])
    except SystemExit:
        pass
    else:
        raise AssertionError


@pytest.mark.timeout(2)
def test_read_next(lexer, test):
    """checks Lexer.read_next"""
    lexer.i = Stream(
        """
pisz 4
"""
    )

    test(lexer.read_next(), EOL())

    test(lexer.read_next(), Statement("pisz", Int(4)))

    try:
        test(lexer.read_next(), EOL())
    except EndOfFile:
        pass


@pytest.mark.timeout(2)
def test_read_indent(lexer):
    """Checks Lexer.read_indent"""
    lexer.i = Stream("    pisz 4")

    lexer.read_indent()

    if lexer.i.col != 4:
        raise AssertionError


@pytest.mark.timeout(2)
def test_read_indent_block(lexer):
    """Checks Lexer.read_indent_block"""
    lexer.i = Stream(
        """    pisz 4

    # pisz 2
    pisz 5"""
    )
    indent_block = lexer.read_indent_block()
    if not compare_list(
        indent_block,
        [
            Statement("pisz", args=Int(4)),
            EOL(),
            EOL(),
            EOL(),
            Statement("pisz", args=Int(5)),
            EOL(),
        ],
    ):
        print(indent_block)
        raise AssertionError

    lexer.i = Stream("\tpisz 4\n\n\tpisz 5")
    lexer.indent_char = None
    lexer.indent_size = None

    indent_block = lexer.read_indent_block()
    if not compare_list(
        indent_block,
        [
            Statement("pisz", args=Int(4)),
            EOL(),
            EOL(),
            Statement("pisz", args=Int(5)),
            EOL(),
        ],
    ):
        print(indent_block)
        raise AssertionError


@pytest.mark.timeout(2)
def test_read_indent_size(lexer):
    """Checks Lexer.read_indent_size"""
    lexer.i = Stream("    test")
    lexer.read_indent_size()

    if lexer.indent_size != 4 or lexer.indent_char != " ":
        raise AssertionError

    lexer.i = Stream("\ttest")
    lexer.indent_char = None
    lexer.indent_size = None
    lexer.read_indent_size()

    if lexer.indent_size != 1 or lexer.indent_char != "\t":
        raise AssertionError


@pytest.mark.timeout(2)
def test_table_init(lexer):
    lexer.i = Stream("[1, 2]")

    try:
        lexer.read_next()
    except SystemExit:
        pass
    else:
        raise AssertionError

