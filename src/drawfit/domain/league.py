from typing import List, Tuple, NoReturn, Dict
from datetime import datetime

import drawfit.domain.notifications as notf
from drawfit.domain.followables import Game, Team 

from drawfit.utils import Sites, OddSample, LeagueCode, LeagueCode, LeagueCodeError


class League:

    def __init__(self, name: str):
        
        self._name: str = name
        self._active: bool = True

        self._current_games: List[Game] = []

        self._followed_teams: List[Team] = []
        self._inactive_teams: List[Team] = []

        self._league_codes: Dict[Sites, LeagueCode] = {site: None for site in Sites}

    @property
    def name(self) -> str:
        return self._name
    
    @property
    def active(self) -> bool:
        return self._active

    @property
    def current_games(self) -> List[Game]:
        return self._current_games

    @property
    def followed_teams(self) -> List[Team]:
        return self._followed_teams
    
    @property
    def inactive_teams(self) -> List[Team]:
        return self._inactive_teams
    
    @property
    def codes(self) -> List[LeagueCode]:
        return self._league_codes
    
    def setCode(self, code: LeagueCode) -> NoReturn:
        self._league_codes[code.getSite()] = code

    def registerGame(self, name: str, date: datetime = None) -> NoReturn:
        new_game = Game(name, date)
        if new_game not in self.current_games:
            self._current_games.append(new_game)
        
    def addGameKeywords(self, game_name: str, keywords: List[str]) -> bool:

        game = next((game for game in self.current_games if game.name == game_name), None)

        if game is not None:
            game.addKeywords(keywords)
            return True
        
        return False

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
                self.inactive_teams.append(team)
                self.followed_teams.pop(index)
                break
    
    def activate_team(self, team_name: str) -> NoReturn:
        for index, team in enumerate(self.inactive_teams):
            if team.name == team_name:
                self.followed_teams.append(team)
                self.inactive_teams.pop(index)
                break
    
    def setTeamId(self, team_name: str, team_id: Tuple[str], site: Sites) -> NoReturn:

        team = next((team for team in self.followed_teams if team.name == team_name), None)
        if team is not None:
            team.setId(site, team_id)
            return

        team = next((team for team in self.inactive_teams if team.name == team_name), None)
        if team is not None:
            team.setId(site, team_id)

    def setGameId(self, game_name: str, game_id: Tuple[str], site: Sites) -> NoReturn:
        
        game = next((game for game in self.current_games if game.name == game_name), None)
        if game is not None:
            game.setId(site, game_id)
    
    def updateOdds(self, samples_by_site: Dict[Sites, List[OddSample]]) -> List[notf.Notification]:

        results = []

        for site, site_samples in samples_by_site.items():

            # site is not active or an error ocurred
            if site_samples is None:
                continue

            for sample in site_samples:
                notification = self.processSample(site, sample)

                if notification not in results and notification is not None:
                    results.append(notification)
            
        return results


    def processSample(self, site: Sites, sample: OddSample) -> notf.Notification:

        # 1 - sample's game name is being monitored so the odd is added
        game = next((game for game in self.current_games if game.isId(site, sample.game_id)), None)

        if game is not None:

            if sample.start_time <= sample.sample_time:
                self.current_games.remove(game)
                return None

            if game.addOdd(sample, site):
                return notf.NewOddNotification(game)
            return None


        # 2 - test if the game has a team that is recognized
        team = next((team for team in self.followed_teams if team.isId(site, sample.team1_id) or team.isId(site, sample.team2_id)), None)
        
        if team is not None and sample.start_time >= sample.sample_time:

            game = team.getGameByDate(sample.start_time)

            if game is not None:
                game.setId(site, sample.game_id)
                game.addOdd(sample, site)
                return notf.NewOddNotification(game)

            new_game = Game(sample.game_name, date=sample.start_time)
            new_game.setId(site, sample.game_id)
            
            self._current_games.append(new_game)
            team.addGame(new_game)
            new_game.addOdd(sample, site)

            return notf.NewOddNotification(new_game)

        # 3 - test if the game could belong to a followed team
        for team_name in sample.game_id:

            team_id = (team_name, )
            possible_team = next((team for team in self.followed_teams if team.couldBeId(site, team_id)), None)

            if possible_team is not None:
                possible_team.addConsidered(site, team_id)
                return notf.PossibleTeamNotification(possible_team, sample, team_id, site)
        
        # 4 - test if the game could be a singled out inputed game
        possible_game = next((game for game in self.current_games if game.couldBeId(site, sample.game_id)), None)

        if possible_game is not None:
            possible_game.addConsidered(site, sample.game_id)
            return notf.PossibleGameNotification(possible_game, sample, site)
        
        return None

