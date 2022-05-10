from datetime import datetime
from src.drawfit.domain.classes.Odd import Odd

def test_odd():

    new_odd = Odd(10.0, datetime.now())

    assert new_odd.value == 10
    assert new_odd.date <= datetime.now()