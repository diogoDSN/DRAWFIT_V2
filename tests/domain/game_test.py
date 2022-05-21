import pytest
from datetime import datetime, date

from drawfit.utils import Sites
from drawfit.domain.followables import Game, Team
from drawfit.utils.odd_sample import OddSample

from ..utils import DATE1, DATE2, GAME1, GAME1_ID1, GAME1_ID2, GAME2, ODDS, RUNTIME, SITE1, SITE2


def test_game_constructor():
    game = Game(GAME1, DATE1)

    assert game.name == GAME1
    assert game.date == DATE1
    assert game.odds == {site: [] for site in Sites}

    with pytest.raises(AttributeError):
        game.name = None
    with pytest.raises(AttributeError):
        game.odds = None

def test_game_equals_self():
    game = Game(GAME1, DATE1)
    assert game == game

def test_game_equals_equal_game():

    game = Game(GAME1, DATE1)
    equal_game = Game(GAME1, DATE1)
    equal_game.addOdd(OddSample(GAME1_ID1, ODDS[0], DATE1, RUNTIME), SITE1)
    equal_game.addOdd(OddSample(GAME1_ID2, ODDS[1], DATE1, RUNTIME), SITE2)

    assert game == equal_game

def test_game_equals_different_game():
    game = Game(GAME1, DATE1)
    different_game1 = Game(GAME2, DATE1)
    different_game2 = Game(GAME1, DATE2)
    different_game3 = Game(GAME2, DATE2)

    assert game != different_game1
    assert game != different_game2
    assert game != different_game3

