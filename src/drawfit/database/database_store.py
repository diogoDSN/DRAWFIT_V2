from __future__ import annotations
import asyncio
from typing import Dict, List, Tuple, NoReturn, TYPE_CHECKING, Optional
from psycopg2 import connect, connection
from functools import wraps

if TYPE_CHECKING:
    from drawfit.domain.league import League

import drawfit.domain.notifications as notf
import drawfit.domain.league as l
from drawfit.dtos import LeagueDto, DomainDto
from drawfit.database.drawfit_database_error import DrawfitDatabaseError
from drawfit.database.db_messages import *

from drawfit.utils import Sites, OddSample, LeagueCode

class DatabaseStore:
    
    def __init__(self) -> NoReturn:
        # No caching
        self._db_connection = None
    
    def __enter__(self) -> DatabaseStore:
        self._db_connection = connect(dbname='drawfit_mock', user='drawfit_bot', host='localhost', password='McMahaeWsNoBeat')
        return self

    def __exit__(self) -> NoReturn:
        self._db_connection.rollback()
        self._db_connection.close()
        self._db_connection = None
    
    @property
    def db_connection() -> Optional[connection]:
        return _db_connection

    def getAllSites() -> List[str]:
        with self.db_connection.cursor() as cursor:
            cursor.execute("SELECT * FROM site;")
            stored_sites = cursor.fetchall()
        
        return [site for site in Sites if (site.value,) in stored_sites]


    def getAllColors() -> Tuple[Tuple[str, int]]:
        with self.db_connection.cursor() as cursor:
            cursor.execute("SELECT * FROM color;")
            stored_colors = cursor.fetchall()
        
        return tuple(color_tuple for color_tuple in stored_colors)
        

    def getLeague(self, league_name: str, ghost: bool =False) -> Optional[League]:
        with self.db_connection.cursor() as cursor:
            
            cursor.execute("SELECT * FROM league WHERE name=(%s);", (league_id))
            result = cursor.fetchall()
            if len(result) != 1:
                raise DrawfitDatabaseError(LeagueNotFound(league_id))
            
            league = l.League(result[0][0])
            league.color = result[0][1]
            
            cursor.execute("SELECT site_name, code FROM league_code WHERE league_name = (%s);", (league_id))
            
            
            
            if ghost:
                return league
            

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
