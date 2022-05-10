from domain.classes.League import League

class LeagueDto:

    def __init__(self, league: League):
        
        self.name = league.name
        self.active = league.active