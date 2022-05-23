from __future__ import annotations
import asyncio
from typing import Dict, List, Tuple, NoReturn, TYPE_CHECKING

if TYPE_CHECKING:
    from drawfit.domain.league import League

import drawfit.domain.notifications as notf
import drawfit.domain.league as l
from drawfit.dtos import LeagueDto

from drawfit.utils import Sites, OddSample, LeagueCode

class DomainStore:

    def __init__(self) -> NoReturn:
        self.known_leagues = []

    def getLeague(self, league_id: str) -> League:
        try:
            index = int(league_id)-1
            
            if index >= len(self.known_leagues):
                return None
            
            return self.known_leagues(index)

        except ValueError:
            return next((league for league in self.known_leagues if league.name == league_id), None)

    
    def addLeague(self, league_name: str) -> NoReturn:

        league = next((league for league in self.known_leagues if league.name == league_name), None)

        if league is None:
            self.known_leagues.append(l.League(league_name))


    def removeLeague(self, league_id: str) -> NoReturn:

        league = self.getLeague(league_id)

        if league is not None:
            self.known_leagues.remove(league)
            
    def changeLeagueCode(self, league_id: str, site: Sites, newCode: str):

        league = self.getLeague(league_id)

        if league is not None:
            league.codes[site] = newCode

    def getLeagues(self) -> List:

        leagues = []

        for league in self.known_leagues:
            leagues.append(LeagueDto(league.name, league.active))
        
        return leagues
    
    def getLeagueCodes(self, leagueName: str) -> List:

        league = next((league for league in self.known_leagues if league.name == leagueName), None)

        if league is None:
            return []

        return league.codes.copy()

    def getAllLeagueCodes(self) -> Dict[str, List[str]]:

        result = {}

        for league in self.known_leagues:
            result[league.name] = league.codes.copy()
        
        return result

    def updateLeaguesOdds(self, results: Dict[str, List[List[OddSample]]]) -> List[notf.Notification]:

        notifications = []

        for league_id, odds_sample in results.items():
            league = next(league for league in self.known_leagues if league.name == league_id)
            notifications.extend(league.updateOdds(odds_sample))
        
        return notifications

    def setTeamId(self, team_name: str, team_id: Tuple[str], site: Sites, league_name: str):
        league = next((league for league in self.known_leagues if league.name == league_name), None)
        if league != None:
            league.setTeamId(team_name, team_id, site)

    def setGameId(self, game_name: str, game_id: Tuple[str], site: Sites, league_name: str):
        league = next((league for league in self.known_leagues if league.name == league_name), None)
        if league != None:
            league.setGameId(game_name, game_id, site)
    
    def setLeagueCode(self, league_name: str, code: LeagueCode) -> NoReturn:

        try:
            league_number = int(league_name)-1

            if league_number < len(self.known_leagues):
                self.known_leagues[league_number].setCode(code)

        except ValueError:
            league = next((league for league in self.known_leagues if league.name == league_name), None)

            if league != None:
                league.setCode(code)
    
    def registerTeam(self, league_id: str, team_name: str) -> bool:

        league = self.getLeague(league_id)

        if league is None:
            return False
        
        return league.registerTeam(team_name)
    
    def addTeamKeywords(self, league_id: str, team_name: str, keywords: List[str]) -> bool:

        league = self.getLeague(league_id)

        if league is None:
            return False
        
        return league.addTeamKeywords(team_name, keywords)