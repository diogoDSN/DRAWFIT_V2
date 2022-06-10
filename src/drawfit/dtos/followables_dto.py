from __future__ import annotations

from typing import TYPE_CHECKING
from drawfit.utils import Sites


if TYPE_CHECKING:
    from drawfit.domain.followables import Followable, Game, Team

from drawfit.dtos.odd_dto import OddDto


class FollowableDto:

    def __init__(self, followable: Followable):
        self.keywords = {}
        self.considered = {}
        self.ids = followable.ids.copy()
        self.complete = followable.complete

        for site in Sites:
            self.keywords = followable.keywords.copy()
            self.considered[site] = followable.considered[site].copy()

class GameDto(FollowableDto):

    def __init__(self, game: Game):
        super().__init__(game)

        self.name = game.name
        self.date = game.date
        self.team1 = None if game.team1 is None else game.team1.name
        self.team2 = None if game.team2 is None else game.team2.name

        self.odds = {}

        for site in Sites:
            self.odds[site] = []
            for odd in game.odds[site]:
                self.odds[site].append(OddDto(odd))

class TeamDto(FollowableDto):

    def __init__(self, team: Team):
        super().__init__(team)

        self.name = team.name
        self.active = team.active
        self.current_game = None if team.current_game is None else GameDto(team.current_game)




