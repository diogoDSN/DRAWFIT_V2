import pytest
from datetime import datetime, date

from drawfit.utils import Sites
from drawfit.domain.followables import Game, Team
from drawfit.utils.odd_sample import OddSample

from ..utils import DATE1, DATE2, GAME1, GAME1_BWIN_ID, GAME1_BETANO_ID, GAME2, ODDS, RUNTIME, BWIN, BETANO


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
    equal_game.addOdd(OddSample(GAME1_BWIN_ID, ODDS[0], DATE1, RUNTIME), BWIN)
    equal_game.addOdd(OddSample(GAME1_BETANO_ID, ODDS[1], DATE1, RUNTIME), BETANO)

    assert game == equal_game

def test_game_equals_different_game():
    game = Game(GAME1, DATE1)
    different_game1 = Game(GAME2, DATE1)
    different_game2 = Game(GAME1, DATE2)
    different_game3 = Game(GAME2, DATE2)

    assert game != different_game1
    assert game != different_game2
    assert game != different_game3

