"""This module contains tests for pseudo.type.bool"""

import pytest
from pseudo.type.bool import Bool, read_bool


@pytest.mark.timeout(2)
def test_read_bool():
    """Checks read_bool"""
    if read_bool("prawda") != Bool(1):
        raise AssertionError
    if read_bool("fałsz") != Bool(0):
        raise AssertionError
