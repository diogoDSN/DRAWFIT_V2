from __future__ import annotations
import asyncio
from typing import Dict, List, Tuple, NoReturn, TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from drawfit.domain.league import League
    from drawfit.domain.followables import Team

import drawfit.domain.notifications as notf
import drawfit.domain.league as l
import drawfit.database.database_store as d
from drawfit.dtos import LeagueDto, DomainDto

from drawfit.utils import Sites, OddSample, LeagueCode

class DomainStore:


    #----------------------------------------------------------------------
    #-------------- Initialization Methods
    #----------------------------------------------------------------------

    def __init__(self) -> NoReturn:
        self.db_store = d.DatabaseStore()
        
        with self.db_store as db:
            # set all valid colors
            DomainStore.colors_list = db.getAllColors()
        
        self.teams = []
        
        # fetch all leagues and teams
        self.leagues = {league.name: league for league in self.loadAllLeagues()}
        self.teams = {team.name: team for team in self.loadAllTeams()}

        # fetch current game for each team if any
        with self.db_store as db:
            for team in self.teams.values():
                team.current_game = db.getCurrentGame(team.name)    
    
    def loadAllLeagues(self) -> List[League]:
        with self.db_store as db:
            # fetch leagues
            leagues = db.getAllLeagues()
            
            # add registered teams to corresponding leagues
            for league in leagues:
                team_names = db.getTeamNamesFromLeague(league.name)
                
                for team_name in team_names:
                    if team_name in self.teams:
                        league.addTeam(self.teams[team_name])
                        self.teams[team_name].addLeague(league)
        
        return leagues
    
    def loadAllTeams(self) -> List[Team]:
        with self.db_store as db:
            # fetch leagues
            teams = db.getAllTeams()
            
            # add registered teams to corresponding leagues
            for team in teams:
                league_names = db.getLeagueNamesFromTeam(team.name)
                
                for league_name in league_names:
                    if league_name in self.leagues:
                        team.addLeague(self.leagues[league_name])
                        self.leagues[league_name].addTeam(team)
        
        return teams
    
    #----------------------------------------------------------------------
    #-------------- Update Methods
    #----------------------------------------------------------------------
    
    def updateLeaguesOdds(self, results: Dict[str, List[List[OddSample]]]) -> List[notf.Notification]:

        notifications = []

        for league_name, odd_samples in results.items():
            league = self.getLeague(league_name)
            notifications.extend(league.UpdateOdds(odds_sample))
        
        return notifications
    
    #----------------------------------------------------------------------
    #-------------- Registration Methods
    #----------------------------------------------------------------------
    
    def registerLeague(self, league_name: str) -> None:
        with self.db_store as db:
            db.registerLeague(league_name, 0xfffff)
            self.leagues[league_name] = db.getLeague(league_name)
        
    
    def registerTeam(self, team_name: str) -> None:
        with self.db_store as db:
            db.registerTeam(team_name)
            self.teams[team_name] = db.getTeam(team_name)
    
    def registerLeagueCode(self, league_name: str, site: Site, code: LeagueCode) -> None:
        with self.db_store as db:
            if self.leagues[league_name].codes[site] is None:
                db.addLeagueCode(league_name, site, str(code))
            else:
                db.updateLeagueCode()
        
        self.leagues[league_name].setCode(code)
    
    
    
        
    
    #----------------------------------------------------------------------
    #-------------- Old Store
    #----------------------------------------------------------------------


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

    def changeLeagueCode(self, league_id: str, site: Sites, newCode: LeagueCode) -> bool:

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