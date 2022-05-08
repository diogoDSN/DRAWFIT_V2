import asyncio
from typing import Dict, List, NoReturn

from domain.classes.Sites import Sites
from domain.classes.League import League

from dtos.LeagueDto import LeagueDto
from updates.sites.utils import OddSample

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

    def getLeagues(self) -> List:

        leagues = []

        for league in self.knownLeagues:
            leagues.append(LeagueDto(league))
        
        return leagues
    
    def getLeagueCodes(self, leagueName: str) -> List:
        try:

            league = next(league for league in self.knownLeagues if league.name == leagueName)
            return league.leagueCodes.copy()

        except StopIteration:
            return []

    def getAllLeagueCodes(self) -> Dict[str, List[str]]:

        result = {}

        for league in self.knownLeagues:
            result[league.name] = league.league_codes.copy()
        
        return result

    def updateLeaguesOdds(self, results: Dict[str, List[List[OddSample]]]) -> NoReturn:
        for league_id, odds_sample in results.items():
            league = next(league for league in self.knownLeagues if league.name == league_id)
            league.updateOdds(odds_sample)