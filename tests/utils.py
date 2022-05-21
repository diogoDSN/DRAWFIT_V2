from datetime import datetime, timedelta

from drawfit.utils import Sites


SITE1 = Sites.Bwin
SITE2 = Sites.Betano

LEAGUE1 = 'Taça de Portugal'

GAME1 = 'Benfica vs Porto'
GAME1_ID1 = ('Benfica', 'FC Porto')
GAME1_ID2 = ('Sport Lisboa Benfica', 'FC Porto')
GAME1_ID3 = ('Benfica', 'Porto')

GAME2 = 'Sporting vs Braga'
GAME2_ID1 = ('Sporting', 'Braga')
GAME2_ID2 = ('Sporting Clube de Portugal', 'Braga')
GAME2_ID3 = ('Sporting', 'Sporting de Braga')

TEAM1 = 'Porto'
TEAM1_ID = ('FC Porto', )

TEAM2 = 'Benfica'
TEAM2_ID = ('Sport Lisboa Benfica', )

TEAM3 = 'Sporting'
TEAM3_ID = ('Sporting', )

TEAM3 = 'Braga'
TEAM3_ID = ('Braga', )

NO_MATCH_TEAM = 'this_team_doesn\'t_belong'
NO_TEAM_ID = (NO_MATCH_TEAM, )

ODDS = [1.4, 1.3, 2.0, 3.2, 2.5]

RUNTIME = datetime.now().replace(second=0, microsecond=0)

DATE1 = RUNTIME + timedelta(days=14, hours=4)
DATE2 = RUNTIME + timedelta(days=7, hours=35)

