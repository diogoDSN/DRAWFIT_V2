def SiteNotFound(name: str) -> str:
    return f'The given site: [{name}], was not found in the database.'

def ColorNotFound(name: str) -> str:
    return f'The given color: [{name}] was not found in the database.'

def LeagueNotFound(name: str) -> str:
    return f'The given league: [{name}], was not found in the database.'

def TeamNotFound(name: str) -> str:
    return f'The given team: [{name}], was not found in the database.'

def GameNotFound(name: str, date: str) -> str:
    return f'The given game: [{name}] at date [{date}], was not found in the database.'

def DuplicateLeague(name: str) -> str:
    return f'Tried to register a duplicate league name: [{name}].'

def DuplicateTeam(name: str) -> str:
    return f'Tried to register a duplicate team name: [{name}].'

def InvalidColor(value: int) -> str:
    return f'The given color value: [{value}], is invalid.'

def DuplicateOdd(game_name: str, site_name: str, odd_date: str) -> str:
    return f'The game [{game_name}] already has an odd registered for [{site_name}] at [{odd_date}].'

def TeamAlreadyHasGame(team_name: str, game_date: str) -> str:
    return f'The team [{team_name}] already has a game on [{game_date}].'

def GameAlreadyRegistered(game_name: str, game_date: str) -> str:
    return f'There is a game with the name [{game_name}] already registered for date [{game_date}].'

def TeamNotInLeague(team_name: str, league_name: str) -> str:
    return f'The team [{team_name}] doesn\'t play in the league [{league_name}].'

def DuplicateLeagueCode(league_name: str, site_name: str) -> str:
    return f'The league [{league_name}] already has a code registered for the site [{site_name}].'

def RepeatedSiteCode(site_name: str, code: str) -> str:
    return f'The site [{site_name}] already has a the code [{code}] registered.'

def DuplicateTeamId(team_name: str, site_name: str) -> str:
    return f'The team [{team_name}] already has an id registered for the site [{site_name}].'

def DuplicateGameId(game_name: str, game_date: str, site_name: str) -> str:
    return f'The game [{game_name}] at date [{game_date}] already has an id registered for the site [{site_name}].'