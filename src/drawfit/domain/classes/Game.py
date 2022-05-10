from typing import NoReturn, List

from domain.classes.Sites import Sites
import domain.classes.Team as team
from domain.classes.Odd import Odd
from updates.sites.utils import OddSample

from datetime import datetime

class Game:

    def __init__(self, name: str, date: datetime, keywords: List[str] = [], team: team.Team = None):

        # Set universal undefined values
        self.name: str = name
        self.date: datetime = date
        self.keywords: List[str] = keywords
        self.team = team

        # Set undefined values dependant on site
        self.considered_games = []
        self.site_names = []
        self.odds = []

        for _ in Sites:
            self.site_names.append(None)
            self.odds.append([0])
            self.considered_games([])
        
    @property
    def date(self) -> datetime:
        return self.date

    @property
    def names(self) -> str:
        return self.site_names
    
    def addConsideredGame(self, site: Sites, team1: str, team2: str) -> NoReturn:
        self.considered_games[site.value].append((team1, team2))
    
    def removeConsideredGame(self, site: Sites, team1: str, team2: str) -> NoReturn:
        self.considered_games[site.value].remove((team1, team2))

    def couldBeGame(self, team1: str, team2: str, site: Sites) -> bool:

        if self.site_names[site.value] is not None or (team1, team2) in self.considered_games[site.value]:
            return False

        for keyword in self.keywords:
            if keyword in team1 or team1 in keyword \
            or keyword in team2 or team2 in keyword:
                return True
        
        return False
                

    def addOdd(self, sample: OddSample, site: Sites) -> Odd:

        if self.odds[site.value][-1].value != sample.odd:
            self.odds[site.value].append(Odd(sample.odd, sample.sample_time))
            return self.odds[site.value][-1]
        
        return None
        
        