from domain.classes.Sites import Sites

class PossibleGameNotification:

    def __init__(self, game_name: str, possible_name: str, league_name: str, site: Sites):

        self.game_name: str = game_name
        self.possible_name: str = possible_name
        self.league_name: str = league_name
        self.site: Sites = site

    def __str__(self):
        return f''