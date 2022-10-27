from __future__ import annotations
import asyncio
from typing import Dict, List, Tuple, NoReturn, TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from drawfit.domain.league import League

import drawfit.domain.notifications as notf
import drawfit.domain.league as l
from drawfit.dtos import LeagueDto, DomainDto

from drawfit.utils import Sites, OddSample, LeagueCode

class DomainStore:

    colors_list = (
        ('White', 0xFFFFFF),
        ('Red', 0xFF0000),
        ('Orange', 0xFF7000),
        ('Yellow', 0xFFFF00),
        ('Cyan', 0x42D4F4),
        ('Blue', 0x4363D8),
        ('Navy', 0x000075),
        ('Green', 0x3CB44B),
        ('Lime', 0xBFEF45),
        ('Mint', 0xAAFFC3),
        ('Pink', 0xF032E6),
        ('Purple', 0x800080),
        ('Lavender', 0xDCBEFF),
        ('Maroon', 0x800000),
        ('Olive', 0x808000),
        ('Apricot', 0xFFD8B1),
        ('Brown', 0x9A6324),
        ('Gray', 0x808080)
    )

    def __init__(self) -> NoReturn:
        self.known_leagues = []

    def getLeague(self, league_id: str) -> Optional[League]:
        try:
            index = int(league_id)-1
            
            if index >= len(self.known_leagues):
                return None
            
            return self.known_leagues[index]

        except ValueError:
            return next((league for league in self.known_leagues if league.name == league_id), None)


    async def removeRoutine(self) -> NoReturn:
        while True:
            await asyncio.sleep(3600)
            for league in self.known_leagues:
                league.removeRoutine()

    def addLeague(self, league_name: str) -> NoReturn:

        league = next((league for league in self.known_leagues if league.name == league_name), None)

        if league is None:
            self.known_leagues.append(l.League(league_name))
    

    def eraseLeague(self, league_id: str) -> bool:

        league = self.getLeague(league_id)

        if league is not None:
            self.known_leagues.remove(league)
            return True
        
        return False

    def changeLeagueCode(self, league_id: str, site: Sites, newCode: str) -> bool:

        league = self.getLeague(league_id)

        if league is not None:
            league.codes[site] = newCode
            return True
        
        return False

    def changeLeagueColor(self, league_id: str, new_color: int) -> bool:

        league = self.getLeague(league_id)

        if league is not None and 0 <= new_color < len(DomainStore.colors_list):
            league.color = DomainStore.colors_list[new_color][1]
            return True
        
        return False

    def getDomain(self) -> DomainDto:
        return DomainDto(self.known_leagues)

    def getLeagues(self) -> List:

        leagues = []

        for league in self.known_leagues:
            leagues.append(LeagueDto(league.name, league.active))
        
        return leagues
    
    def getLeagueCodes(self, leagueName: str) -> List:

        league = self.getLeague(leagueName)

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

    def activateTeam(self, league_id: str, team_id: str) -> bool:
        league = self.getLeague(league_id)

        if league is not None:
            return league.activateTeam(team_id)
        else:
            return False

    def deactivateTeam(self, league_id: str, team_id: str) -> bool:
        
        league = self.getLeague(league_id)

        if league is not None:
            return league.deactivateTeam(team_id)
        else:
            return False

    def eraseTeam(self, league_id: str, team_id: str) -> bool:

        league = self.getLeague(league_id)

        if league is not None:
            return league.eraseTeam(team_id)
        else:
            return False
    
    def eraseId(self, league_id: str, team_id: str, id_to_erase: str) -> bool:

        league = self.getLeague(league_id)

        if league is not None:
            return league.eraseId(team_id, id_to_erase)
        
        return False

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