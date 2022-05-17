import pytest
from datetime import datetime

from drawfit.domain import Odd

from ..utils import get_fixed_date, ODDS


# Arranje
@pytest.fixture(autouse=True)
def create_odd(get_fixed_date):
    return Odd(ODDS[0], get_fixed_date)


def test_constructor(create_odd, get_fixed_date):

    odd = create_odd
    assert odd.value == ODDS[0]
    assert odd.date == get_fixed_date

def test_equals(create_odd, get_fixed_date):

    assert create_odd == Odd(ODDS[0], get_fixed_date)
    assert create_odd != Odd(ODDS[1], get_fixed_date)
    assert create_odd != Odd(ODDS[0], datetime.now())