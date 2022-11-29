from __future__ import annotations

import asyncio

from typing import List, Tuple, NoReturn, Dict, Set, TYPE_CHECKING
from datetime import datetime

import drawfit.domain.notifications as notf
from drawfit.domain.followables import Game, Team 

if TYPE_CHECKING:
    from drawfit.database.database_store import DatabaseStore

from drawfit.utils import Sites, OddSample, LeagueCode, LeagueCode, LeagueCodeError, now_lisbon


class League:

    def __init__(self, name: str, color: int = 0xffffff):
        
        self._name: str = name
        self._color: int = color

        self._current_games: List[Game] = []

        self._teams: Dict[str, Team] = {}
        self._inactive_teams: List[Team] = []

        self._league_codes: Dict[Sites, LeagueCode] = {site: None for site in Sites}

    @property
    def name(self) -> str:
        return self._name
    
    @property
    def color(self) -> int:
        return self._color
    
    @color.setter
    def color(self, color: int) -> NoReturn:
        self._color = color

    @property
    def current_games(self) -> List[Game]:
        return self._current_games

    @property
    def teams(self) -> Dict[str, Team]:
        return self._teams
    
    @property
    def inactive_teams(self) -> List[Team]:
        return self._inactive_teams
    
    @property
    def codes(self) -> List[LeagueCode]:
        return self._league_codes

    def addTeam(self, team: Team) -> NoReturn:
        self._teams[team.name] = team
    
    def setCode(self, code: LeagueCode) -> NoReturn:
        self._league_codes[code.getSite()] = code

    def registerTeam(self, name: str) -> bool:

        if next((team for team in self.followed_teams if team.name == name), None) is None and next((team for team in self.inactive_teams if team.name == name), None) is None:
            self._followed_teams.append(Team(name))
            return True
        
        return False
    
    def addTeamKeywords(self, team_name: str, keywords: List[str]) -> bool:

        team = next((team for team in self.followed_teams if team.name == team_name), None)


        if team is not None:
            team.addKeywords(keywords)
            return True
        
        team = next((team for team in self.inactive_teams if team.name == team_name), None)

        if team is not None:
            team.addKeywords(keywords)
            return True
        
        return False
    
    def eraseTeam(self, team_name) -> bool:

        for index, team in enumerate(self.followed_teams):
            if team.name == team_name:
                self.followed_teams.pop(index)
                return True
        
        for index, team in enumerate(self.inactive_teams):
            if team.name == team_name:
                self.inactive_teams.pop(index)
                return True
        
        return False
    
    def setTeamId(self, team_name: str, team_id: Tuple[str], site: Sites, db_store: DatabaseStore) -> NoReturn:

        team = next((team for team in self.teams.values() if team.name == team_name), None)
        if team is not None:
            with db_store as db:
                db.addTeamId(team_name, site, team_id)
            team.setId(site, team_id)
            return
    
    def eraseId(self, team_name: str, id_to_erase: str) -> bool:

        for _, team in enumerate(self.followed_teams):
            if team.name == team_name:
                team.eraseId(id_to_erase)
                return True
        
        for _, team in enumerate(self.inactive_teams):
            if team.name == team_name:
                team.eraseId(id_to_erase)
                return True
        
        return False