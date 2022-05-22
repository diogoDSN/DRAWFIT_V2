import pytest
from datetime import datetime, date

from drawfit.utils import Sites
from drawfit.utils.odd_sample import OddSample

from ..utils import DATE1, GAME1_BWIN_ID, RUNTIME, TEAM1, TEAM1_BWIN_ID, TEAM2, ODDS, TEAM2_BWIN_ID


def test_odd_sample_constructor():
    odd_sample = OddSample(GAME1_BWIN_ID, ODDS[0], DATE1, RUNTIME)

    assert odd_sample.game_id == GAME1_BWIN_ID
    assert odd_sample.odd == ODDS[0]
    assert odd_sample.start_time == DATE1
    assert odd_sample.sample_time == RUNTIME
    assert odd_sample.team1_id == TEAM2_BWIN_ID
    assert odd_sample.team2_id == TEAM1_BWIN_ID
    assert odd_sample.game_name == f'{TEAM2_BWIN_ID[0]} vs {TEAM1_BWIN_ID[0]}'
    assert odd_sample.team1_name == TEAM2_BWIN_ID[0]
    assert odd_sample.team2_name == TEAM1_BWIN_ID[0]

    with pytest.raises(AttributeError):
        odd_sample.game_id = None
    with pytest.raises(AttributeError):
        odd_sample.odd = None
    with pytest.raises(AttributeError):
        odd_sample.start_time = None
    with pytest.raises(AttributeError):
        odd_sample.sample_time = None
    with pytest.raises(AttributeError):
        odd_sample.team1_id = None
    with pytest.raises(AttributeError):
        odd_sample.team2_id = None
    with pytest.raises(AttributeError):
        odd_sample.game_name = None
    with pytest.raises(AttributeError):
        odd_sample.team1_name = None
    with pytest.raises(AttributeError):
        odd_sample.team2_name = None
    








    