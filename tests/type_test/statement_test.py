"""This module contains tests for pseudo.type.Statement"""

import pytest

from pseudo.runtime import RunTime
from pseudo.type import Statement


@pytest.mark.timeout(2)
def test_exit():
    try:
        Statement("koniec").eval(RunTime())
    except SystemExit:
        pass
    else:
        raise AssertionError
