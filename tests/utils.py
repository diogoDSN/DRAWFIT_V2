from datetime import datetime, timedelta

from drawfit.utils import Sites


BWIN = Sites.Bwin
BETANO = Sites.Betano

LEAGUE1 = 'Taça de Portugal'



TEAM1 = 'Porto'
TEAM1_BWIN_ID = ('FC Porto', )
TEAM1_BETANO_ID = ('FC Porto', )

TEAM2 = 'Benfica'
TEAM2_BWIN_ID = ('Benfica', )
TEAM2_BETANO_ID = ('Sport Lisboa Benfica', )

TEAM3 = 'Sporting'
TEAM3_BWIN_ID = ('Sporting Clube de Portugal', )
TEAM3_BETANO_ID = ('Sporting', )

TEAM4 = 'Braga'
TEAM4_BWIN_ID = ('Braga', )
TEAM4_BETANO_ID = ('Sporting de Braga', )

NO_MATCH_TEAM = 'this_team_doesn\'t_belong'
NO_TEAM_ID = (NO_MATCH_TEAM, )

GAME1 = 'Benfica vs Porto'
GAME1_BWIN_ID = (TEAM2_BWIN_ID[0], TEAM1_BWIN_ID[0])
GAME1_BETANO_ID = (TEAM1_BETANO_ID[0], TEAM2_BETANO_ID[0])

GAME2 = 'Sporting vs Benfica'
GAME2_BWIN_ID = (TEAM3_BWIN_ID[0], TEAM2_BWIN_ID[0])
GAME2_BETANO_ID = (TEAM3_BETANO_ID[0], TEAM2_BETANO_ID[0])

GAME3 = 'Portela vs Mucifal'
GAME2_BWIN_ID = ('Portela de Sintra', 'Clube do Mucifal')
GAME2_BETANO_ID = ('Portela', 'Mucifal')

ODDS = [1.4, 1.3, 2.0, 3.2, 2.5]

RUNTIME = datetime.now().replace(second=0, microsecond=0)

DATE1 = RUNTIME + timedelta(days=14, hours=4)
DATE2 = RUNTIME + timedelta(days=7, hours=35)

