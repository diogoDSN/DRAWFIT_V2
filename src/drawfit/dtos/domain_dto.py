from __future__ import annotations
from typing import Dict, NoReturn, TYPE_CHECKING

import discord

if TYPE_CHECKING:
    from drawfit.domain.league import League
    from drawfit.domain.followables import Team

import drawfit.dtos.league_dto as l
import drawfit.dtos.followables_dto as f

class DomainDto:

    def __init__(self, leagues: Dict[str, League], teams: Dict[str, Team]) -> NoReturn:

        leagues_dtos = {}
        teams_dtos = {}

        for league in leagues.values():
            leagues_dtos[league.name] = l.LeagueDto(league)
        
        for team in teams.values():
            teams_dtos[team.name] = f.TeamDto(team)
    
        self.leagues = list(leagues_dtos.values())
        self.leagues.sort(key= lambda league: league.name.lower())
        self.teams = list(teams_dtos.values())
        self.teams.sort(key= lambda team: team.name.lower())
        
        for team in self.teams:
            for league in self.leagues:
                if leagues[league.name] in teams[team.name].leagues.values():
                    league.teams.append(team)
                    team.leagues.append(league)
            if not teams[team.name].current_game is None:
                team.current_game.league = next(league for league in team.leagues \
                    if league.name == teams[team.name].current_game.league.name \
                    )
