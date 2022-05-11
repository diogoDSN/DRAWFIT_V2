from drawfit.domain import League

class LeagueDto:

    def __init__(self, league_name: str, active: bool):
        
        self.name = league_name
        self.active = active