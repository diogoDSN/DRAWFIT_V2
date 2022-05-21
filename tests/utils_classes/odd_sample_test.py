import pytest
from datetime import datetime, date

from drawfit.utils import Sites
from drawfit.domain.followables import Game, Team

from ..utils import get_fixed_date1, get_fixed_date2, create_odd_sample1, TEAM1, TEAM2, ODDS


def test_odd_sample_constructor( get_fixed_date1, get_fixed_date2, create_odd_sample1):
    odd_sample = create_odd_sample1
    start = get_fixed_date1
    sample = get_fixed_date2

    assert odd_sample.game_id == (TEAM1, TEAM2)
    assert odd_sample.odd == ODDS[0]
    assert odd_sample.start_time == start
    assert odd_sample.sample_time == sample







    