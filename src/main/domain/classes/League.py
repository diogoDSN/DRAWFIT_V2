#from domain.classes.Team import Team
#from domain.classes.Team import Game


from domain.classes.Sites import Sites


class League:

    def __init__(self, name: str):
        
        self.name = name
        self.leagueCodes = []
        self.currentGames = []
        self.followedTeams = []
        self._active = True

        for site in Sites:
            self.leagueCodes.append(None)

    @property
    def active(self) -> bool:
        return self._active

''' 
    @property
    def currentGames(self) -> list[Game]:
        return self.currentGames

    @property
    def followedTeams(self) -> list[Team]:
        return self.followedTeams
'''