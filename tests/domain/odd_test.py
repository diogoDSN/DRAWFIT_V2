import pytest
from datetime import datetime

from drawfit.domain.odd import Odd

from ..utils import DATE1, ODDS, RUNTIME


def test_odd_constructor():

    odd = Odd(ODDS[0], RUNTIME)
    assert odd.value == ODDS[0]
    assert odd.date == RUNTIME

def test_odd_equals():

    odd = Odd(ODDS[0], RUNTIME)

    assert odd == Odd(ODDS[0], RUNTIME)
    assert odd != Odd(ODDS[1], RUNTIME)
    assert odd != Odd(ODDS[0], DATE1)
