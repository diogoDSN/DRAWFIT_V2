from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from drawfit.domain.league import League

from drawfit.dtos.followables_dto import GameDto, TeamDto


class LeagueDto:

    def __init__(self, league: League):

        self.name = league.name
        self.active = league.active
        self.color = league.color
        self.codes = league.codes

        self.followed_teams = []

        for team in league.followed_teams:
            self.followed_teams.append(TeamDto(team))
        
        self.inactive_teams = []

        for team in league.inactive_teams:
            self.inactive_teams.append(TeamDto(team))
        
        self.current_games = []

        for game in league.current_games:
            self.current_games.append(GameDto(game))