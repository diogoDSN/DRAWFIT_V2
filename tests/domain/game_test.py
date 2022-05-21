import pytest
from datetime import datetime, date

from drawfit.utils import Sites
from drawfit.domain.followables import Game, Team

from ..utils import get_fixed_date1, create_game, create_odd_sample1, create_odd_sample2, GAME1, SITE1, SITE2


def test_game_constructor(create_game, get_fixed_date1):
    game = create_game

    assert game.name == GAME1
    assert game.date == get_fixed_date1
    assert game.odds == {site: [] for site in Sites}

    with pytest.raises(AttributeError):
        game.name = None
    with pytest.raises(AttributeError):
        game.odds = None

def test_game_equals_same_game(create_game):
    game = create_game
    assert game == game

def test_game_equals_equal_game(create_odd_sample1, create_odd_sample2, create_game, get_fixed_date1):

    game = create_game
    equal_game = Game(GAME1, get_fixed_date1)
    equal_game.addOdd(create_odd_sample1, SITE1)
    equal_game.addOdd(create_odd_sample2, SITE2)

    assert game == equal_game
