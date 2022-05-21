import pytest
from datetime import datetime

from drawfit.domain.odd import Odd

from ..utils import get_fixed_date1, ODDS


# Arranje
@pytest.fixture(autouse=True)
def create_odd(get_fixed_date1):
    return Odd(ODDS[0], get_fixed_date1)


def test_constructor(create_odd, get_fixed_date1):

    odd = create_odd
    assert odd.value == ODDS[0]
    assert odd.date == get_fixed_date1

def test_equals(create_odd, get_fixed_date1):

    assert create_odd == Odd(ODDS[0], get_fixed_date1)
    assert create_odd != Odd(ODDS[1], get_fixed_date1)
    assert create_odd != Odd(ODDS[0], datetime.now())
