from typing import List, NoReturn

from drawfit.domain import Team, Game
from drawfit.utils import Sites, OddSample


class League:

    def __init__(self, name: str):
        
        self.name: str = name
        self.league_codes: List[str] = []
        self.active: bool = True

        self.current_games: List[Game] = []

        self.followed_teams: List[Team] = []

        for _ in Sites:
            self.league_codes.append(None)

    @property
    def active(self) -> bool:
        return self.active
    
    def deactivate(self) -> NoReturn:
        self.active = False
    
    def activate(self) -> NoReturn:
        self.active = True

    @property
    def currentGames(self) -> List[Game]:
        return self.current_games

    @property
    def followedTeams(self) -> List[Team]:
        return self.followed_teams


    def updateOdds(self, samples_by_site: List[List[OddSample]]) -> NoReturn:

        results = [[] for _ in Sites]

        for site in Sites:

            # site is not active or an error ocurred
            if samples_by_site[site.value] is None:
                pass

            for sample in samples_by_site[site.value]:
                results[site.value].append(self.processSample(site, sample))
            
        return results


    def processSample(self, site: Sites, sample: OddSample):

        # sample's game name is being monitored so the odd is added
        game = next((game for game in self.current_games if game.names[site.value] == sample.gameId), None)

        if game is not None:
            return game.addOdd(sample, site)


        # test if the game has a team that is recognized
        team = next((team for team in self.followed_teams if team.isTeam(site, sample.team1) or team.isTeam(site, sample.team2)), None)
        
        if team is not None:
            new_game = Game(sample.game_id, sample.game_time, team=team)
            new_game.site_name(site, sample.game_id)
            
            self.current_games.append(new_game)

            return new_game.addOdd(sample, site)


        # test if the game could belong to a followed team
        possible_team1 = next((team for team in self.followed_teams if team.couldBeTeam(site, sample.team1)), None)
        possible_team2 = next((team for team in self.followed_teams if team.couldBeTeam(site, sample.team2)), None)

        if possible_team1 is not None:
            possible_team1.addConsideredName(site, sample.team1)
            #TODO
            #return PossibleTeamNotification(possible_team.name, sample.team1, self.name, sample.game_id, site)
        
        if possible_team2 is not None:
            possible_team1.addConsideredName(site, sample.team2)
            #TODO
            #return PossibleTeamNotification(possible_team.name, sample.team2, self.name, sample.game_id, site)

        # test if the game could be an singled out inputed game
        possible_game = next((game for game in self.current_games if game.couldBeGame(sample.team1, sample.team2)), None)

        if possible_game is not None:
            possible_game.addConsideredGame(site, sample.team1, sample.team2)
            #TODO
            #return PossibleGameNotification(possible_game.name, sample.game_id, self.name, site)
        
        return None

