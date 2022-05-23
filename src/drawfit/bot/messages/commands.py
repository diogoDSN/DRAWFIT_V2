def EmptyArgument(command: str):
    return f'This command takes no arguments. Correct usage:\n```.{command}```'

def removeLeagueUsage():
    return 'Correct usage:\n```.removeLeague (league_name|league_number)```'

def addLeagueUsage():
    return 'Correct usage:\n```.addLeague (league_name)```'

def addTeamUsage():
    return 'Correct usage:\n```.addTeam (league_name)::(team_name)```'

def addTeamKeywordsUsage():
    return 'Correct usage:\n```.addTeamKeywords (league_name)::(team_name)::(keyword1) (keyword2) (keyword3) ...```'

def setBwinLeagueCodeUsage():
    return 'Correct usage:\n```.setBwinLeagueCode (region_id),(competition_id) (league_name|league_number)```'

def setBetanoLeagueCodeUsage():
    return 'Correct usage:\n```.setBetanoLeagueCode (league_id) (league_name|league_number)```'

def setSolverdeLeagueCodeUsage():
    return 'Correct usage:\n```.setSolverdeLeagueCode (country_code),(league_id) (league_name|league_number)```'

def setMooshLeagueCodeUsage():
    return 'Correct usage:\n```.setMooshLeagueCode (league_id)::(league_name|league_number)```'

def setBetwayLeagueCodeUsage():
    return 'Correct usage:\n```.setBetwayLeagueCode (league_id)::(league_name|league_number)```'

def setBetclicLeagueCodeUsage():
    return 'Correct usage:\n```.setBetclicLeagueCode (league_id) (league_name|league_number)```'


    