from domain.Team import Team
from domain.Team import Game


class League:

    def __init__(self, name: str, leagueCodes: list):
        
        self.name = name
        self.leagueCodes = leagueCodes
        self.currentGames = []
        self.followedTeams = []
        self.active = True

    @property
    def active(self) -> bool:
        return self.active
    
    @property
    def currentGames(self) -> list:
        return self.currentGames

    @property
    def followedTeams(self) -> list:
        return self.followedTeams
