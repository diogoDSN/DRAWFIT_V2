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
        
        self.teams = []
        
        # fetch all leagues and teams
        self.leagues = {league.name: league for league in self.loadAllLeagues()}
        self.teams = {team.name: team for team in self.loadAllTeams()}

        # fetch current game for each team if any
        with self.db_store as db:
            for team in self.teams.values():
                team.current_game = db.getCurrentGame(team) 
    
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
            league = self.leagues[league_name]
            notifications.extend(league.updateOdds(odd_samples, self.db_store))
        
        return notifications
    
    #----------------------------------------------------------------------
    #-------------- Write Methods
    #----------------------------------------------------------------------
    
    def registerLeague(self, league_name: str) -> NoReturn:
        with self.db_store as db:
            db.registerLeague(league_name, 0xfffff)
        
        self.leagues[league_name] = db.getLeague(league_name)
    
    def registerTeam(self, team_name: str) -> NoReturn:
        with self.db_store as db:
            db.registerTeam(team_name)
        
        self.teams[team_name] = db.getTeam(team_name)
    
    def setLeagueCode(self, league_name: str, site: Site, code: LeagueCode) -> NoReturn:
        with self.db_store as db:
            if self.leagues[league_name].codes[site] is None:
                db.addLeagueCode(league_name, site, str(code))
            else:
                db.updateLeagueCode(league_name, site, str(code))
        
        self.leagues[league_name].setCode(code)
    
    def setLeagueColor(self, league_name: str, color_name: str) -> NoReturn:
        with self.db_store as db:
            new_color = db.getColor(color_name)
            db.updateLeagueColor(league_name, new_color)
        
        self.leagues[league_name].color = new_color
    
    
    def addTeamToLeague(self, team_name: str, league_name: str) -> NoReturn:
        with self.db_store as db:
            db.addTeamToLeague(team_name, league_name)
        
        team = self.teams[teams_name]
        league = self.leagues[league_name]
        team.leagues[league_name] = league
        league.teams[team_name] = team
    
    def addTeamKeywords(self, team_name: str, keywords: List[str]) -> NoReturn:
        self.teams[team_name].addKeywords(keywords)
    
    def activateTeam(self, team_name: str) -> NoReturn:
        with self.db_store as db:
            db.activateTeam(team_name)
        
        self.teams

    def deactivateTeam(self, league_id: str, team_id: str) -> bool:
        
        league = self.getLeague(league_id)

        if league is not None:
            return league.deactivateTeam(team_id)
        else:
            return False
    
        
    #----------------------------------------------------------------------
    #-------------- Read Methods
    #----------------------------------------------------------------------
    
    def getAllLeagueCodes(self) -> Dict[str, List[str]]:

        result = {}

        for league in self.leagues.values():
            result[league.name] = league.codes.copy()
        
        return result

    
    #----------------------------------------------------------------------
    #-------------- Old Store
    #----------------------------------------------------------------------


    async def removeRoutine(self) -> NoReturn:
        while True:
            await asyncio.sleep(3600)
            # TODO remove past games and erase their ids from the db
    

    def eraseLeague(self, league_id: str) -> bool:

        league = self.getLeague(league_id)

        if league is not None:
            self.known_leagues.remove(league)
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
    