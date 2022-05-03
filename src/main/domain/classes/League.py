from domain.classes.Team import Team
from domain.classes.Team import Game


class League:

    def __init__(self, name: str, leagueCodes: list[str]):
        
        self.name = name
        self.leagueCodes = leagueCodes
        self.currentGames = []
        self.followedTeams = []
        self.active = True

    @property
    def active(self) -> bool:
        return self.active
    
    @property
    def currentGames(self) -> list[Game]:
        return self.currentGames

    @property
    def followedTeams(self) -> list[Team]:
        return self.followedTeams
