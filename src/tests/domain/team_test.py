import pytest

from drawfit.utils import Sites
from drawfit.domain.followables import Team

from ..utils import  TEAM1


def test_team_constructor():

    team = Team(TEAM1)

    assert team.name == TEAM1

    with pytest.raises(AttributeError):
        team.name = None
