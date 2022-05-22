import pytest
from drawfit.domain.followables import Team
from drawfit.domain.league import League
from drawfit.domain.notifications import PossibleTeamNotification

from drawfit.utils import Sites
from drawfit.utils.odd_sample import OddSample

from ..utils import BETANO, BWIN, DATE1, GAME1, GAME1_BETANO_ID, GAME1_BWIN_ID, GAME2_BWIN_ID, GAME3, LEAGUE1, ODDS, RUNTIME, TEAM1, TEAM1_BWIN_ID, TEAM2, TEAM2_BWIN_ID, TEAM3


@pytest.fixture(scope="function")
def create_demo_league():
    league = League(LEAGUE1)
    league.registerTeam(TEAM1)
    league.addTeamKeywords(TEAM1, [TEAM1])
    league.registerTeam(TEAM2)
    league.addTeamKeywords(TEAM2, [TEAM2])

    league.registerGame(GAME3)
    league.addGameKeywords(GAME3, [GAME3.split(' vs ')[0], GAME3.split(' vs ')[1]])

    return league

def test_league_constructor():
    
    league = League(LEAGUE1)

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


def test_register_team():

    league = League(LEAGUE1)

    league.registerTeam(TEAM1)
    league.registerTeam(TEAM2)

    assert len(league.followed_teams) == 2
    assert league.followed_teams[0].name == TEAM1
    assert league.followed_teams[1].name == TEAM2

def test_league_add_team_keywords():
    
    league = League(LEAGUE1)

    print(f'\n{league.followed_teams}\n')

    league.registerTeam(TEAM1)
    league.registerTeam(TEAM2)

    print(f'\n{league.followed_teams}\n')

    league.addTeamKeywords(TEAM1, ["key1", "key2"])

    print(f'\n{league.followed_teams}\n')

    assert "key1" in league.followed_teams[0].keywords
    assert "key2" in league.followed_teams[0].keywords
    assert len(league.followed_teams[0].keywords) == 2
    assert league.followed_teams[1].keywords == []

def test_possible_team(create_demo_league):

    league = create_demo_league

    sample = OddSample(GAME1_BWIN_ID, ODDS[0], DATE1, RUNTIME)

    update = {site: None for site in Sites}
    update[BWIN] = [sample]

    notifications = league.updateOdds(update)

    assert notifications == [PossibleTeamNotification(league.followed_teams[1], sample, TEAM2_BWIN_ID, BWIN)]

def test_possible_team_two_teams(create_demo_league):

    league = create_demo_league

    sample = OddSample(GAME1_BWIN_ID, ODDS[0], DATE1, RUNTIME)

    update = {site: None for site in Sites}
    update[BWIN] = [sample]

    notifications1 = league.updateOdds(update)
    notifications2 = league.updateOdds(update)

    

    assert notifications1 == [PossibleTeamNotification(league.followed_teams[1], sample, TEAM2_BWIN_ID, BWIN)]
    assert notifications2 == [PossibleTeamNotification(league.followed_teams[0], sample, TEAM1_BWIN_ID, BWIN)]
