import pytest

from drawfit.utils import Sites

from ..utils import create_league, create_team, LEAGUE1, TEAM1


def test_league_constructor(create_league):
    
    league = create_league

    assert league.name == LEAGUE1
    assert league.current_games == []
    assert league.followed_teams == []
    assert league.inactive_teams == []
    assert league.codes == {site: None for site in Sites}

    with pytest.raises(AttributeError):
        league.name = None
    with pytest.raises(AttributeError):
        league.current_games = None
    with pytest.raises(AttributeError):
        league.followed_teams = None
    with pytest.raises(AttributeError):
        league.inactive_teams = None
    with pytest.raises(AttributeError):
        league.codes = None

def test_league_add_team_keywords(create_league):
    
    league = create_league
    
    league.registerTeam(TEAM1)
    league.addTeamKeywords(TEAM1, ["key1", "key2"])

    assert "key1" in league.followed_teams[0].keywords
    assert "key2" in league.followed_teams[0].keywords
    assert len(league.followed_teams[0].keywords) == 2

