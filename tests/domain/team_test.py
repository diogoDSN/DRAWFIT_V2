import pytest

from drawfit.utils import Sites
from drawfit.domain import Team

from ..utils import get_fixed_date, create_team, TEAM1


def test_constructor(create_team, get_fixed_date):

    team = create_team

    assert team.name == TEAM1

    # assert followanle __init__ called
    assert team.keywords == []
    assert team.considered == [[] for _ in Sites]
    assert team.ids == [None for _ in Sites]
    assert team.complete == False

    with pytest.raises(AttributeError):
        team.name = None
