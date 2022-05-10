from domain.classes.Sites import Sites

class PossibleTeamNotification:

    def __init__(self, team_name: str, possible_name: str, league_name: str, game: str, site: Sites):

        self.team_name: str = team_name
        self.possible_name: str = possible_name
        self.league_name: str = league_name
        self.game: str = game
        self.site: Sites = site