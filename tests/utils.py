import pytest
from datetime import datetime

from drawfit.utils import Sites
from drawfit.domain.followables import Game, Team
from drawfit.domain.league import League
from drawfit.utils import OddSample


SITE1 = Sites.Bwin
SITE2 = Sites.Betano

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
def get_fixed_date1():
    return datetime.now()

@pytest.fixture(scope="session")
def get_fixed_date2():
    return datetime.now()

@pytest.fixture(scope="session")
def get_fixed_date3():
    return datetime.now()

@pytest.fixture(scope="session")
def get_fixed_date4():
    return datetime.now()

@pytest.fixture
def create_game(get_fixed_date1):
    return Game(GAME1, get_fixed_date1)

@pytest.fixture
def create_team():
    return Team(TEAM1)

@pytest.fixture
def create_league():
    return League(LEAGUE1)

@pytest.fixture(scope="session")
def create_odd_sample1(get_fixed_date1, get_fixed_date2):
    return OddSample((TEAM1, TEAM2), ODDS[0], get_fixed_date1, get_fixed_date2)

@pytest.fixture(scope="session")
def create_odd_sample2(get_fixed_date3, get_fixed_date4):
    return OddSample((TEAM1, TEAM2), ODDS[1], get_fixed_date3, get_fixed_date4)
