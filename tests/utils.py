import pytest
from datetime import datetime

from drawfit.utils import Sites
from drawfit.domain import Game, Team, League


SITE1 = Sites.BWIN
SITE2 = Sites.BETANO

LEAGUE1 = 'Taça de Portugal'

GAME1 = 'Benfica - Porto'
GAME1_ID = ('Benfica', 'FC Porto')

TEAM1 = 'Porto'
TEAM1_ID = ('FC Porto', )

TEAM2 = 'Benfica'
TEAM2_ID = ('Sport Lisboa Benfica', )

NO_MATCH_TEAM = 'this_team_doesn\'t_belong'
NO_TEAM_ID = (NO_MATCH_TEAM, )

ODDS = [1.4, 1.3, 2.0, 3.2, 2.5]



@pytest.fixture(scope="session")
def get_fixed_date():
    return datetime.now()


@pytest.fixture
def create_game(get_fixed_date):
    return Game(GAME1, get_fixed_date)

@pytest.fixture
def create_team():
    return Team(TEAM1)

@pytest.fixture
def create_league():
    return League(LEAGUE1)
