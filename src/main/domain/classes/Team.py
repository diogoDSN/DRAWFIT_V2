from domain.classes.Sites import Sites
from domain.classes.Game import Game


class Team:

    def __init__(self, name: str, knownSearchNames: list[str]):
        
        self.name = name
        self.knowSearchNames = knownSearchNames
        self.games = []

        # Set properties dependent of site
        self.knownNames = []

        for _ in Sites:
            self.knownNames.append(None)
    
    @property
    def games(self) -> list[Game]:
        return self.games
    
    @property
    def name(self) -> str:
        return self.name
