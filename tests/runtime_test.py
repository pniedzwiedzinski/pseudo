"""This module contains tests for `pseudo.runtime`"""

import pytest

from pseudo.runtime import MemoryObject
from pseudo.type.numbers import Int
from pseudo.type.variable import Variable
from pseudo.type import Statement


def test_save(runtime, test):
    runtime.save("a", Int(1))
    test(runtime.var["a"].getter(), 1)

    runtime.save("b[1][1]", Int(5))
    test(runtime.var["b[1][1]"].getter(), 5)


def test_get(runtime, test):
    runtime.var["a"] = MemoryObject("a", 1)

    test(runtime.get("a"), 1)

    runtime.var["b[1]"] = MemoryObject("b[1]", 3)

    test(runtime.get("b[1]"), 3)


def test_stdout(runtime, test, capsys):
    runtime.run([Statement("pisz", Int(1))])

    captured = capsys.readouterr()
    test(captured.out, "1")


def test_stdin(runtime, test, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "Oh, hi Mark")

    runtime.run([Statement("czytaj", Variable("a"))])

    test(runtime.get("a"), "Oh, hi Mark")

    monkeypatch.setattr("builtins.input", lambda _: "1")

    runtime.run([Statement("czytaj", Variable("b"))])

    test(runtime.get("b"), 1)


def test_throw(runtime):
    try:
        runtime.throw("error")
    except SystemExit:
        pass
    else:
        raise AssertionError
