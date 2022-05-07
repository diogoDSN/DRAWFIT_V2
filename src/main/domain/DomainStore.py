import asyncio
from typing import NoReturn

from domain.classes.Sites import Sites
from domain.classes.League import League

from dtos.LeagueDto import LeagueDto

class DomainStore:

    def __init__(self) -> NoReturn:
        self.knownLeagues = []
        self.n_sites = len(Sites.__members__)

    def addLeague(self, leagueName: str) -> NoReturn:

        if list(filter(lambda league: league.name == leagueName, self.knownLeagues)) == []:
            self.knownLeagues.append(League(leagueName))
    
    def removeLeague(self, leagueId: str) -> NoReturn:

        try:
            index = int(leagueId)-1
            
            if index >= len(self.knownLeagues):
                return

            self.knownLeagues.pop(index)
            
        except ValueError:
            try:
                self.knownLeagues.remove(next(league for league in self.knownLeagues if league.name == leagueId))
            except StopIteration:
                pass
            
    def changeLeagueCode(self, leagueName: str, index: int, newCode: str):

        try:
            if index >= self.n_sites:
                return

            league = next(league for league in self.knownLeagues if league.name == leagueName)

            league.leagueCodes[index] = newCode


        except StopIteration:
            pass

    def getLeagues(self) -> list:

        leagues = []

        for league in self.knownLeagues:
            leagues.append(LeagueDto(league))
        
        return leagues
    
    def getLeagueCodes(self, leagueName: str) -> list:
        try:

            league = next(league for league in self.knownLeagues if league.name == leagueName)
            return league.leagueCodes.copy()

        except StopIteration:
            return []

