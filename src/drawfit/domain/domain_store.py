from __future__ import annotations
import asyncio
from typing import Dict, List, Tuple, NoReturn, TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from drawfit.domain.league import League
    from drawfit.domain.followables import Team

import drawfit.domain.notifications as notf
import drawfit.domain.league as l
import drawfit.domain.followables as f
import drawfit.database.database_store as d
from drawfit.dtos import LeagueDto, DomainDto
from drawfit.database.drawfit_error import DrawfitError
from drawfit.database.db_messages import TeamNotFound, LeagueNotFound, GameAlreadyRegistered

from drawfit.utils import Sites, OddSample, LeagueCode, now_lisbon, str_dates

class DomainStore:
    
    remove_routine_time = 900

    #----------------------------------------------------------------------
    #-------------- Initialization Methods and Properties
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
                team.current_game = db.getCurrentGame(team, self.leagues) 
    
    @property
    def colors_list(self) -> Tuple[Tuple(str, int)]:
        with self.db_store as db:
            return db.getAllColors()
    
    def loadAllLeagues(self) -> List[League]:
        with self.db_store as db:
            # fetch leagues
            leagues = db.getAllLeagues()
        
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
    #-------------- Routines Methods
    #----------------------------------------------------------------------
    
    def updateLeaguesOdds(self, results: Dict[str, Dict[Sites, List[OddSample]]]) -> List[notf.Notification]:

        notifications = []

        for league_name, odd_samples in results.items():
            notifications.extend(self.updateOdds(self.leagues[league_name], odd_samples))
        
        return notifications
    
    def updateOdds(self, league: l.League, samples_by_site: Dict[Sites, List[OddSample]]) -> List[notf.Notification]:

        results = []

        for site, site_samples in samples_by_site.items():
            # site is not active or an error ocurred
            if site_samples is None:
                continue

            for sample in site_samples:
                notification = self.processSample(league, site, sample)

                if notification not in results and notification is not None:
                    results.append(notification)
                elif notification is not None:
                    results[results.index(notification)].mergeNotifications(notification)
                        
        return results


    def processSample(self, league: l.League, site: Sites, sample: OddSample) -> notf.Notification:
        # 1 - sample's game name is being monitored so the odd is added
        team = next((team for team in league.teams.values() \
                if (team.active) and (not team.current_game is None) and team.current_game.isId(site, sample.game_id)\
                    ), None)

        if team is not None:
            game = team.current_game

            # Odd after game start
            if sample.start_time <= sample.sample_time:
                team.current_game = None
                return None
            
            # New date
            if game.canUpdateDate(sample):
                self.updateGameDate(game, sample.start_time)
                return notf.DateChangeNotification(game, site, league.color)

            if game.canAddOdd(sample.odd, sample.sample_time, site):
                with self.db_store as db:
                    db.registerOdd(game.name, game.date, site, sample.odd, sample.sample_time)
                # Add odd to game
                if game.addOdd(sample.odd, sample.sample_time, site):
                    return notf.NewOddNotification(game, site, league.color)
            return None

        # 2 - test if the game has a team that is recognized
        team = next((team for team in self.teams.values() \
                if team.active and (team.isId(site, sample.team1_id) or team.isId(site, sample.team2_id))\
                    ), None)
        
        if team is not None and sample.start_time >= sample.sample_time:

            # Is current game but with different date (may vary by site)
            if team.isCurrentGame(sample.start_time, league):
                game = team.current_game
                with self.db_store as db:
                    db.addGameId(game.name, game.date, site, sample.game_id)
                    if game.canAddOdd(sample.odd, sample.sample_time, site):
                        db.registerOdd(game.name, game.date, site, sample.odd, sample.sample_time)
                
                team.current_game.setId(site, sample.game_id)
                team.current_game.addOdd(sample.odd, sample.sample_time, site)

                return notf.NewOddNotification(team.current_game, site, league.color)

            # Different game at a later date
            if team.hasGame() and team.current_game.date < sample.start_time:
                return None
            
            # Different game earlier than previously registered game
            elif team.hasGame():
                team.current_game = None
            
            new_game = f.Game(sample.game_name, sample.start_time, team, league)
            
            try:

                with self.db_store as db:
                    db.registerGame(team.name, new_game.name, new_game.date, league.name)
                    db.addGameId(new_game.name, new_game.date, site, sample.game_id)
                    db.registerOdd(new_game.name, new_game.date, site, sample.odd, sample.sample_time)
            
            except DrawfitError as e:
                if e.error_message == GameAlreadyRegistered(new_game.name, str_dates(new_game.date)):
                    correct_team_id = sample.team1_id if team.isId(site, sample.team2_id) else sample.team2_id
                    print(f"correct_team_id: {correct_team_id};wrong team: {team.name}: site: {site};")
                    
                    try:
                        possible_team = next(team2 for team2 in self.teams.values() \
                            if team.active and team2.isId(site, correct_team_id))
                        with self.db_store as db:
                            db.addTeamId(correct_team.name, site, correct_team_id)
                            db.addGameId(new_game.name, new_game.date, site, sample.game_id)

                        correct_team.setId(site, correct_team_id)
                        correct_team.current_game.setId(site, sample.game_id)
                        return None
                    except StopIteration:
                        possible_team = next(team2 for team2 in self.teams.values() \
                            if team.active and team2.couldBeId(site, correct_team_id))
                        
                        return notf.PossibleTeamNotification(possible_team.name, sample, correct_team_id, site, league.color, league.name)
                else:
                    raise e

            
            new_game.setId(site, sample.game_id)
            new_game.addOdd(sample.odd, sample.sample_time, site)

            team.current_game = new_game

            return notf.NewOddNotification(new_game, site, league.color)

        # 3 - test if the game could belong to a followed team
        for team_name in sample.game_id:

            team_id = (team_name, )
            possible_team = next((team for team in self.teams.values() if team.couldBeId(site, team_id)), None)

            if possible_team is not None:
                possible_team.addConsidered(site, team_id)
                return notf.PossibleTeamNotification(possible_team.name, sample, team_id, site, \
                    league.color, league.name)
        
        return None


    
    async def removeRoutine(self) -> NoReturn:
        while True:
            await asyncio.sleep(DomainStore.remove_routine_time)
            # TODO add exception logging
            for team in self.teams.values():
                if team.current_game is None:
                    continue
                
                if team.current_game.date < now_lisbon():
                    with self.db_store as db:
                        db.deleteGameIds(team.current_game.name, team.current_game.date)
                    team.current_game = None
    
    #----------------------------------------------------------------------
    #-------------- League Methods
    #----------------------------------------------------------------------
    
    #--- Write Methods
    
    def registerLeague(self, league_name: str) -> NoReturn:
        with self.db_store as db:
            db.registerLeague(league_name, 0xffffff)
            self.leagues[league_name] = db.getLeague(league_name)
    
    def setLeagueCode(self, league_name: str, code: LeagueCode) -> NoReturn:
        try:
            with self.db_store as db:
                if self.leagues[league_name].codes[code.getSite()] is None:
                    db.addLeagueCode(league_name, code.getSite(), str(code))
                else:
                    db.updateLeagueCode(league_name, code.getSite(), str(code))
            
            self.leagues[league_name].setCode(code)
        except KeyError:
            raise DrawfitError(LeagueNotFound(league_name))
        
    def setLeagueColor(self, league_name: str, color_name: str) -> NoReturn:
        try:
            with self.db_store as db:
                new_color = db.getColor(color_name)
                db.updateLeagueColor(league_name, new_color)
            
            self.leagues[league_name].color = new_color
        except KeyError:
            raise DrawfitError(LeagueNotFound(league_name))
    
    def eraseLeague(self, league_name: str) -> NoReturn:

        try:
            with self.db_store as db:
                    
                for game_name, game_date in db.getAllLeagueGamesIds(league_name):
                    db.deleteGameOdds(game_name, game_date)
                    db.deleteGameIds(game_name, game_date)
                    db.deleteGame(game_name, game_date)
                
                db.deleteLeague(league_name)
                    
                for team in self.leagues[league_name].teams:
                    if (not team.current_game is None) and team.current_game.league is self.leagues[league_name]:
                        team.current_game = None
                    
        except KeyError:
            raise DrawfitError(LeagueNotFound(league_name))
    
    #--- Read Methods
    
    def getAllLeagueCodes(self) -> Dict[str, List[str]]:
        result = {}

        for league in self.leagues.values():
            result[league.name] = league.codes.copy()
        
        return result
    
    def getLeagueTotalGames(self, league_name: str) -> int:
        with self.db_store as db:
            return db.getTotalLeagueGames(league_name)
        
        
    #----------------------------------------------------------------------
    #-------------- Team Methods
    #----------------------------------------------------------------------
    
    #--- Write Methods
    
    def registerTeam(self, team_name: str) -> NoReturn:
        with self.db_store as db:
            db.registerTeam(team_name)
            self.teams[team_name] = db.getTeam(team_name)
    
    def addTeamKeywords(self, team_name: str, keywords: List[str]) -> NoReturn:
        try:
            self.teams[team_name].addKeywords(keywords)
        except KeyError:
            raise DrawfitError(TeamNotFound(team_name))
    
    def setTeamId(self, team_name: str, site: Sites, team_id: Tuple[str], league_name: str) -> NoReturn:
        try:
            team = self.teams[team_name]
            
            with self.db_store as db:
                db.addTeamId(team.name, site, team_id)
                
            if not league_name in team.leagues:
                self.addTeamToLeague(team_name, league_name)
            team.setId(site, team_id)
        except KeyError:
            raise DrawfitError(TeamNotFound(team_name))
    
    def removeConsideredId(self, team_name: str, site: Sites, team_id: Tuple[str]) -> NoReturn:
        try:
            self.teams[team_name].removeConsidered(site, team_id)
        except KeyError:
            raise DrawfitError(TeamNotFound(team_name))
    
    def activateTeam(self, team_name: str) -> NoReturn:
        try:
            with self.db_store as db:
                db.activateTeam(team_name)
        
            self.teams[team_name].active = True
        except KeyError:
            raise DrawfitError(TeamNotFound(team_name))

    def deactivateTeam(self, team_name: str) -> NoReturn:
        try:
            with self.db_store as db:
                db.deactivateTeam(team_name)
                if not (game := self.teams[team_name].current_game) is None:
                    db.deleteGameIds(game.name, game.date)
                    db.deleteGameOdds(game.name, game.date)
                    db.deleteGame(game.name, game.date)
        
            self.teams[team_name].current_game = None
            self.teams[team_name].active = False
        except KeyError:
            raise DrawfitError(TeamNotFound(team_name))
    
    def eraseTeam(self, team_name: str) -> NoReturn:
        try:
            with self.db_store as db:
                    
                for game_name, game_date in db.getAllTeamGamesIds(team_name):
                    db.deleteGameOdds(game_name, game_date)
                    db.deleteGameIds(game_name, game_date)
                    db.deleteGame(game_name, game_date)
                
                db.deleteTeamIds(team_name)
                db.deleteTeam(team_name)
                
                team = self.teams[team_name]
                
                team.current_game = None
                
                for league in team.leagues:
                    del league.teams[team_name]
                    if team in league.inactive_teams:
                        league.inactive_teams.remove(team)
                
                del self.teams[team_name]
            
        except KeyError:
            raise DrawfitError(TeamNotFound(team_name))
    
    def resetTeamIds(self, team_name: str) -> bool:
        try:
            with self.db_store as db:
                db.deleteTeamIds(team_name)
                self.teams[team_name].resetIds()
                
        except KeyError:
            raise DrawfitError(TeamNotFound(team_name))
    
    #--- Read Methods
    def getTotalTeamGames(self, team_name: str) -> int:
        with self.db_store as db:
            return db.getTotalTeamGames(team_name)
        
    #----------------------------------------------------------------------
    #-------------- Other Methods
    #----------------------------------------------------------------------

    #--- Write Methods
    
    def addTeamToLeague(self, team_name: str, league_name: str) -> NoReturn:
        with self.db_store as db:
            db.addTeamToLeague(team_name, league_name)
        
        team = self.teams[team_name]
        league = self.leagues[league_name]
        team.leagues[league_name] = league
        league.teams[team_name] = team
    
    def updateGameDate(self, game: f.Game, new_date: datetime) -> NoReturn:
        with self.db_store as db:
            # delete conflicts from foreign key constraints
            db.deleteGameIds(game.name, game.date)
            db.deleteGameOdds(game.name, game.date)
            
            # update date
            db.updateGameDate(game, new_date)
            
            # reregister deleted data
            for site, odds_list in game.odds.itmes():
                for odd in odds_list:
                    db.registerOdd(game.name, new_date, site, odd.value, odd.date)
                    
            for game_id in game.ids.values():
                if not game_id is None:
                    db.addGameId(game.name, game.date, site, game_id)
                    
        game.date = new_date
    
    #--- Read Methods
    
    def getDomain(self) -> DomainDto:
        return DomainDto(self.leagues, self.teams)
    