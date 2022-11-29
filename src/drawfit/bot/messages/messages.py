def NoPermission(needed: str):
    return f'You do not have permission to do this.\nTo execute this command you need `{needed}` permissions.'

def eraseLeagueConfirmation(league_name: str, games_deleted: int) -> str:
    return f'Are you sure that you want to delete the league **{league_name}**?\nAll games from this league in the present and the past will also be deleted along with their odds!\nThis includes **{games_deleted}** games! (yes/no)'

def eraseTeamConfirmation(team_name: str, games_deleted: int) -> str:
    return f'Are you sure that you want to delete the team **{team_name}**?\nAll games from this team in the present and the past will also be deleted along with their odds!\nThis includes **{games_deleted}** games! (yes/no)'

def TimedOut():
    return "The request has timed out."

def Yes():
    return "✅"

def No():
    return "❌"