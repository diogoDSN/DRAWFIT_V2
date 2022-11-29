from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from drawfit.domain.league import League

from drawfit.dtos.followables_dto import GameDto, TeamDto


class LeagueDto:

    def __init__(self, league: League):

        self.name = league.name
        self.color = league.color
        self.codes = league.codes

        self.teams = []