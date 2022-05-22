import pytest

from drawfit.domain.followables import Game, Team
from drawfit.domain.notifications import NewOddNotification, PossibleGameNotification, PossibleTeamNotification
from drawfit.utils.odd_sample import OddSample

from ..utils import BETANO, BWIN, GAME1, GAME1_BETANO_ID, GAME2, DATE1, DATE2, GAME2_BETANO_ID, GAME2_BWIN_ID, ODDS, GAME1_BWIN_ID, RUNTIME, TEAM1, TEAM2


def test_new_odd_notification_equals():

    game1 = Game(GAME1, DATE1)
    game2 = Game(GAME2, DATE2)
    
    n = NewOddNotification(Game(GAME1, DATE1))

    game1.addOdd(OddSample(GAME1_BWIN_ID, ODDS[0], DATE1, RUNTIME), BWIN)
    game1.addOdd(OddSample(GAME1_BETANO_ID, ODDS[1], DATE1, RUNTIME), BETANO)

    n1 = NewOddNotification(game1)
    n2 = NewOddNotification(game2)

    assert n == n1
    assert n != n2

def test_possible_game_notification_equals():

    game = Game(GAME1, DATE1)
    sample1 = OddSample(GAME1_BWIN_ID, ODDS[0], DATE1, RUNTIME)
    sample2 = OddSample(GAME1_BETANO_ID, ODDS[1], DATE1, RUNTIME)

    n = PossibleGameNotification(game, sample1, BWIN)
    n1 = PossibleGameNotification(game, sample1, BWIN)
    n2 = PossibleGameNotification(game, sample2, BETANO)

    assert n == n1
    assert n != n2


def test_possible_team_notification_equals():

    team = Team(TEAM2)
    sample1 = OddSample(GAME1_BWIN_ID, ODDS[0], DATE1, RUNTIME)
    sample2 = OddSample(GAME2_BWIN_ID, ODDS[1], DATE1, RUNTIME)
    sample3 = OddSample(GAME2_BETANO_ID, ODDS[1], DATE1, RUNTIME)

    n = PossibleTeamNotification(team, sample1, sample1.team1_id, BWIN)
    n1 = PossibleTeamNotification(team, sample2, sample2.team2_id, BWIN)
    n2 = PossibleTeamNotification(team, sample3, sample3.team2_id, BETANO)


    print("\n\n\n\n")
    print(n)
    print("------------------------------------------")
    print(n1)
    print("\n\n\n\n")

    assert n == n1
    assert n != n2