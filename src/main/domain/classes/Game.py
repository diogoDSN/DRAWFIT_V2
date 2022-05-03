from domain.classes.Sites import Sites
from domain.classes.Team import Team
from domain.classes.Odd import Odd

from datetime import datetime

class Game:

    def __init__(self, date: datetime, team1: Team, team2: Team):

        # Set universal undefined values
        self.date = date
        self.teams = [team1, team2]

        # Set undefined values dependant on site
        self.name = []        
        self.gameCode = []
        self.odds = []
        self.beingMonitored = []

        for site in Sites:
            self.odds.append([])
            self.beingMonitored.append(False)
            self.name.append(None)
            self.gameCode.append(None)
        
    @property
    def date(self) -> datetime:
        return self.date
    
    @property
    def teams(self) -> list:
        return [self.team1, self.team2]

    @property
    def names(self) -> str:
        return self.names

    @names.setter
    def names(self, nameSite: tuple):
        name, site = nameSite
        self.names[site.value] = name

    def setAsBeingMonitored(self, site: Sites):
        self.beingMonitored[site.value] = True


    def isBeingMonitored(self, site: Sites) -> bool:
        return self.beingMonitored[site.value]


    def addOdd(self, value: float, site: Sites) -> bool:

        if self.odds[site.value][len(self.odds)-1].value != value:
            self.odds.append(Odd(value, datetime.now(), self))
            return True
        
        return False
        
        