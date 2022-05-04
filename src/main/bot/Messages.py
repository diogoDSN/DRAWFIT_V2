def EmptyArgument(command: str):
    return f'This command takes no arguments. Correct usage:\n```${command}```'

def removeLeagueUsage():
    return 'Correct usage:\n```$removeLeague (name|number of league)```'

def addLeagueUsage():
    return 'Correct usage:\n```$addLeague (name of new league)```'

def NoPermission(needed: str):
    return f'You do not have permission to do this.\nTo execute this command you need {needed} permissions.'