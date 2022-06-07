from __future__ import annotations
from typing import List, NoReturn, TYPE_CHECKING

import discord

if TYPE_CHECKING:
    from drawfit.domain.league import League

import drawfit.dtos.league_dto as l

class DomainDto:

    def __init__(self, leagues: List[League]) -> NoReturn:

        self.known_leagues = []

        for league in leagues:
            self.known_leagues.append(l.LeagueDto(league))
    
    def getLeague(self, number: int) -> Optional[LeagueDto]:
        if 0 <= number < len(self.known_leagues):
            return self.known_leagues[number]
        return None


