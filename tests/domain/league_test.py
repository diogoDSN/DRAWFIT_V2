import pytest

from drawfit.utils import Sites

from ..utils import create_league, LEAGUE1


def test_constructor(create_league):
    
    league = create_league

    assert league.name == LEAGUE1
    assert league.current_games == []
    assert league.followed_teams == []
    assert league.inactive_teams == []
    assert league.league_codes == [None for _ in Sites]

    with pytest.raises(AttributeError):
        league.name = None
    with pytest.raises(AttributeError):
        league.current_games = None
    with pytest.raises(AttributeError):
        league.followed_teams = None
    with pytest.raises(AttributeError):
        league.inactive_teams = None
    with pytest.raises(AttributeError):
        league.league_codes = None
    

