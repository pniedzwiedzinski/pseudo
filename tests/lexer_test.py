"""This module contains unit tests for lexer module."""

import pytest
import pseudo

from pseudo.pseudo_types import Operation, Operator, Int

__author__ = "Patryk Niedźwiedziński"


@pytest.fixture
def lexer():
    """Returns lexer object."""
    lex = pseudo.lexer.Lexer("")
    return lex


def test_is_keyword(lexer):
    """Check Lexer.is_keyword"""
    if not (
        lexer.is_keyword("pisz") is True
        and lexer.is_keyword("oo") is False
        and lexer.is_keyword("koniec") is True
    ):
        raise AssertionError


def test_is_alphabet(lexer):
    """Check Lexer.is_alphabet"""
    if not (
        lexer.is_alphabet("a") is True
        and lexer.is_alphabet("A") is True
        and lexer.is_alphabet("1") is False
        and lexer.is_alphabet("*") is False
        and lexer.is_alphabet(1) is False
    ):
        raise AssertionError


def test_is_digit(lexer):
    """Check Lexer.is_digit"""
    if not (
        lexer.is_digit("1") is True
        and lexer.is_digit("a") is False
        and lexer.is_digit('"') is False
    ):
        raise AssertionError


def test_is_operator(lexer):
    """Checks Lexer.is_operator"""
    if not (
        lexer.is_operator("*") is True
        and lexer.is_operator("div") is True
        and lexer.is_operator(":=") is False
        and lexer.is_operator("pisz") is False
    ):
        raise AssertionError


def test_is_not_keyword_end(lexer):
    """Checks Lexer.is_not_keyword_end"""
    if not (
        lexer.is_not_keyword_end("a") is True
        and lexer.is_not_keyword_end("+") is False
        and lexer.is_not_keyword_end("!") is False
    ):
        raise AssertionError


def test_update_args(lexer):
    """Checks Lexer.update_args"""
    if not (
        lexer.update_args([Int(2), Operator("+"), Int(2)], 1)
        == [Operation(Operator("+"), Int(2), Int(2))]
    ):
        raise AssertionError


def test_read_number(lexer):
    """Checks Lexer.read_number"""
    lexer.i = pseudo.stream.Stream("123")
    if 123 != lexer.read_number().value:
        raise AssertionError
    lexer.i = pseudo.stream.Stream("abc")
    if lexer.read_number() is not None:
        raise AssertionError


def test_read_string(lexer):
    """Checks Lexer.read_string"""
    lexer.i = pseudo.stream.Stream('"abc"')
    if "abc" != lexer.read_string().value:
        raise AssertionError


def test_keyword(lexer):
    """Checks Lexer.read_keyword"""
    lexer.i = pseudo.stream.Stream("pisz x")
    if "pisz" != lexer.read_keyword():
        raise AssertionError


def test_read_args(lexer):
    """Checks Lexer.read_args"""
    lexer.i = pseudo.stream.Stream(" 12")
    if 12 != lexer.read_args().value:
        raise AssertionError
