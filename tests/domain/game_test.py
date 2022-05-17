import pytest
from datetime import datetime, date

from drawfit.utils import Sites
from drawfit.domain import Game, Team

from ..utils import get_fixed_date, create_game, create_team, GAME1, TEAM1, TEAM2, NO_MATCH_TEAM


def test_constructor(create_game, get_fixed_date):
    game = create_game

    assert game.name == GAME1
    assert game.date == get_fixed_date
    assert game.odds == [[] for _ in Sites]

    # assert followable __init__ called
    assert game.keywords == []
    assert game.considered == [[] for _ in Sites]
    assert game.ids == [None for _ in Sites]
    assert game.complete == False

    with pytest.raises(AttributeError):
        game.name = None
    with pytest.raises(AttributeError):
        game.odds = None




    