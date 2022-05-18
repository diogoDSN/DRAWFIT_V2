def EmptyArgument(command: str):
    return f'This command takes no arguments. Correct usage:\n```${command}```'

def removeLeagueUsage():
    return 'Correct usage:\n```$removeLeague (league_name|league_number)```'

def addLeagueUsage():
    return 'Correct usage:\n```$addLeague (league_name)```'

def addTeamUsage():
    return 'Correct usage:\n```$addLeague (team_name)```'

def setBwinLeagueCodeUsage():
    return 'Correctusage:\n```$setBwinLeagueCode region_id competition_id (league_name|league_number)```'