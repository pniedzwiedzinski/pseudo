"""This module contains tests for `pseudo.runtime`"""

import pytest

from pseudo.type.numbers import Int

def test_set_nested_array(runtime, test):
    runtime.var = {"a": {}}
    v = runtime.set_nested_array("a", [Int(1), Int(1)])
    test(runtime.var, {"a": {1: {1: {}}}})
    
    v["x"] = 1
    test(runtime.var["a"][1][1]["x"], 1)

def test_save(runtime, test):
    runtime.save("a", Int(1))
    test(runtime.var["a"], 1)

    runtime.save("b", Int(5), [Int(1), Int(1)])
    test(runtime.var["b"][1][1], 5)

def test_get(runtime, test):
    runtime.var["a"] = 1

    test(runtime.get("a"), 1)

    runtime.var["b"] = {1: {2: 3}}

    test(runtime.get("b", [Int(1), Int(2)]), 3)

def test_throw(runtime):
    try:
        runtime.throw("error")
    except SystemExit:
        pass
    else:
        raise AssertionError
