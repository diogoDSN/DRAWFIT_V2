from datetime import datetime
from drawfit.domain import Odd

def test_oddConstructor():

    new_odd = Odd(10.0, datetime.now())

    assert new_odd.value == 10
    assert new_odd.date <= datetime.now()
