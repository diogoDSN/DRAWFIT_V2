import pytest

from drawfit.utils import Sites
from drawfit.domain.followables import Team

from ..utils import get_fixed_date1, create_team, TEAM1


def test_team_constructor(create_team, get_fixed_date1):

    team = create_team

    assert team.name == TEAM1

    with pytest.raises(AttributeError):
        team.name = None
