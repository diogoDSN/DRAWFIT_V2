from __future__ import annotations
import asyncio
from typing import Dict, List, Tuple, NoReturn, TYPE_CHECKING, Optional
from psycopg2 import connect

if TYPE_CHECKING:
    from drawfit.domain.league import League

import drawfit.domain.notifications as notf
import drawfit.domain.league as l
from drawfit.dtos import LeagueDto, DomainDto

from drawfit.utils import Sites, OddSample, LeagueCode

class DatabaseStore:
    
    def __init__(self) -> NoReturn:
        # No caching
        self.cursor = connect("dbname='template1' user='dbuser' host='localhost' password='dbpass'")

    def getLeague(self, league_id: str) -> Optional[League]:
        try:
            index = int(league_id)-1
            
            if index >= len(self.known_leagues):
                return None
            
            return self.known_leagues[index]

        except ValueError:
            return next((league for league in self.known_leagues if league.name == league_id), None)







    async def removeRoutine(self) -> NoReturn:
        pass

    def addLeague(self, league_name: str) -> NoReturn:
        pass
    
    def eraseLeague(self, league_id: str) -> bool:
        pass

    def changeLeagueCode(self, league_id: str, site: Sites, newCode: str) -> bool:
        pass

    def changeLeagueColor(self, league_id: str, new_color: int) -> bool:
        pass

    def getDomain(self) -> DomainDto:
        pass

    def getLeagues(self) -> List:
        pass
    
    def getLeagueCodes(self, leagueName: str) -> List:
        pass

    def getAllLeagueCodes(self) -> Dict[str, List[str]]:
        pass

    def updateLeaguesOdds(self, results: Dict[str, List[List[OddSample]]]) -> List[notf.Notification]:
        pass

    def activateTeam(self, league_id: str, team_id: str) -> bool:
        pass

    def deactivateTeam(self, league_id: str, team_id: str) -> bool:
        pass

    def eraseTeam(self, league_id: str, team_id: str) -> bool:
        pass
    
    def eraseId(self, league_id: str, team_id: str, id_to_erase: str) -> bool:
        pass

    def setGameId(self, game_name: str, game_id: Tuple[str], site: Sites, league_name: str):
        pass
    
    def setLeagueCode(self, league_name: str, code: LeagueCode) -> NoReturn:
        pass
    
    def registerTeam(self, league_id: str, team_name: str) -> bool:
        pass
    
    def addTeamKeywords(self, league_id: str, team_name: str, keywords: List[str]) -> bool:
        pass