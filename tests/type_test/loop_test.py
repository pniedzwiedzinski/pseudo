"""This module contains test for `pseudo.type.loop`"""

from pseudo import compile
from pseudo.runtime import RunTime

pdc = """
dla i:=1,...,5 wykonuj
    pisz i
    i := i+1
"""


def test_unsettable_iterator():
    instructions = compile(pdc)

    r = RunTime()

    try:
        for i in instructions:
            i.eval(r)
    except SystemExit:
        pass
    else:
        raise AssertionError
