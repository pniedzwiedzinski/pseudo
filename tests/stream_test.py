"""This module contains unit tests for stream module."""

import pytest
import pseudo


__author__ = "Patryk Niedźwiedziński"


@pytest.fixture
def stream():
    """Returns stream object"""

    def _s(i):
        s = pseudo.stream.Stream(i)
        return s

    return _s


def test_next_line(stream):
    """Checks Stream.next_line"""
    s = stream("1\n2")
    s.next_line()
    if "2" != s.peek():
        raise AssertionError


def test_next(stream):
    """Checks Stream.next"""
    s = stream("1\n")
    if "1" != s.next():
        raise AssertionError


def test_eol(stream):
    """Checks Stream.eol"""
    s = stream("\n1\n")
    if not s.eol():
        raise AssertionError
    s.next_line()
    if s.eol():
        raise AssertionError
    s.next()
    if not s.eol():
        raise AssertionError


def test_eof(stream):
    """Checks Stream.eof"""
    s = stream("1")
    if s.eof():
        raise AssertionError
    s.next()
    if not s.eof():
        raise AssertionError
