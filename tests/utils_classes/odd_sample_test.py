import pytest
from datetime import datetime, date

from drawfit.utils import Sites
from drawfit.utils.odd_sample import OddSample

from ..utils import DATE1, GAME1_ID1, RUNTIME, TEAM1, TEAM2, ODDS


def test_odd_sample_constructor():
    odd_sample = OddSample(GAME1_ID1, ODDS[0], DATE1, RUNTIME)

    assert odd_sample.game_id == GAME1_ID1
    assert odd_sample.odd == ODDS[0]
    assert odd_sample.start_time == DATE1
    assert odd_sample.sample_time == RUNTIME







    