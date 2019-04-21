"""This module contains tests for `pseudo.runtime`"""

import pytest

from pseudo.runtime import MemoryObject
from pseudo.type.numbers import Int


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


def test_throw(runtime):
    try:
        runtime.throw("error")
    except SystemExit:
        pass
    else:
        raise AssertionError
