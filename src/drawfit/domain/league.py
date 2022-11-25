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
        

    def deactivateTeam(self, team_name: str) -> NoReturn:
        for index, team in enumerate(self.followed_teams):
            if team.name == team_name:
                team.active = False
                self.inactive_teams.append(team)
                self.followed_teams.pop(index)

                if team.current_game is not None:
                    self.current_games.remove(team.current_game)
                
                team.current_game = None
                return True
        
        return False
    
    def activateTeam(self, team_name: str) -> NoReturn:
        for index, team in enumerate(self.inactive_teams):
            if team.name == team_name:
                team.active = True
                self.followed_teams.append(team)
                self.inactive_teams.pop(index)
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


    def removeGame(self, game: Game) -> NoReturn:
        if game.team1 is not None:
            game.team1.current_game = None
        if game.team2 is not None:
            game.team2.current_game = None
        
        self.current_games.remove(game)

    def removeRoutine(self) -> NoReturn:
        for game in self.current_games:
            if game.date <= now_lisbon():
                self.removeGame(game)


    def updateOdds(self, samples_by_site: Dict[Sites, List[OddSample]], db_store: DatabaseStore) -> List[notf.Notification]:

        results = []

        for site, site_samples in samples_by_site.items():
            # site is not active or an error ocurred
            if site_samples is None:
                continue

            for sample in site_samples:
                notification = self.processSample(site, sample, db_store)

                if notification not in results and notification is not None:
                    results.append(notification)
                elif notification is not None:
                    results[results.index(notification)].mergeNotifications(notification)
                        
        return results


    def processSample(self, site: Sites, sample: OddSample, db_store: DatabaseStore) -> notf.Notification:
        # TODO database integration
        # 1 - sample's game name is being monitored so the odd is added
        team = next((team for team in self.teams.values() \
                if (not team.current_game is None) and team.current_game.isId(site, sample.game_id)\
                    ), None)

        if team is not None:
            game = team.current_game

            # Odd after game start
            if sample.start_time <= sample.sample_time:
                team.current_game = None
                return None
            
            # New date
            if game.canUpdateDate(sample):
                with db_store as db:
                    db.updateGameDate(self, sample.start_time)
                game.updateDate(sample)
                return notf.DateChangeNotification(game, site, self.color)

            if game.canAddOdd(sample.odd, sample.sample_time, site):
                with db_store as db:
                    db.registerOdd(game.name, game.date, site, sample.odd, sample.sample_time)
                # Add odd to game
                if game.addOdd(sample.odd, sample.sample_time, site):
                    return notf.NewOddNotification(game, site, self.color)
            return None

        # 2 - test if the game has a team that is recognized
        team = next((team for team in self.teams.values() \
                if team.isId(site, sample.team1_id) or team.isId(site, sample.team2_id)\
                    ), None)
        
        if team is not None and sample.start_time >= sample.sample_time:

            # Is current game but with different date (may vary by site)
            if team.isGameByDate(sample.start_time):
                game = team.current_game
                with db_store as db:
                    db.addGameId(game.name, game.date, site, sample.game_id)
                    if game.canAddOdd(sample.odd, sample.sample_time, site):
                        db.registerOdd(game.name, game.date, site, sample.odd, sample.sample_time)
                
                team.current_game.setId(site, sample.game_id)
                team.current_game.addOdd(sample.odd, sample.sample_time, site)

                return notf.NewOddNotification(team.current_game, site, self.color)

            # Different game at a later date
            if team.hasGame() and team.current_game.date < sample.start_time:
                return None
            
            # Different game earlier than previously registered game
            elif team.hasGame():
                self.current_games.remove(team.current_game)
            
            new_game = Game(sample.game_name, sample.start_time, team)
            
            with db_store as db:
                db.registerGame(team.name, new_game.name, new_game.date, self.name)
                db.addGameId(new_game.name, new_game.date, site, sample.game_id)
                db.registerOdd(new_game.name, new_game.date, site, sample.odd, sample.sample_time)
            
            new_game.setId(site, sample.game_id)
            new_game.addOdd(sample.odd, sample.sample_time, site)

            self._current_games.append(new_game)
            team.current_game = new_game

            return notf.NewOddNotification(new_game, site, self.color)

        # 3 - test if the game could belong to a followed team
        for team_name in sample.game_id:

            team_id = (team_name, )
            possible_team = next((team for team in self.teams.values() if team.couldBeId(site, team_id)), None)

            if possible_team is not None:
                possible_team.addConsidered(site, team_id)
                return notf.PossibleTeamNotification(possible_team, sample, team_id, site, self.color, db_store)
        
        return None

