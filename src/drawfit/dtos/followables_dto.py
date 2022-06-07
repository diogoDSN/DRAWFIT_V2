from __future__ import annotations

from typing import TYPE_CHECKING
from drawfit.utils import Sites


if TYPE_CHECKING:
    from drawfit.domain.followables import Followable, Game, Team


class FollowableDto:

    def __init__(self, followable: Followable):
        self.keywords = {}
        self.considered = {}
        self.ids = followable.ids.copy()
        self.complete = followable.complete

        for site in Sites:
            self.keywords[site] = followable.keywords[site].copy()
            self.considered[site] = followable.considered[site].copy()

class GameDto(FollowableDto):

    def __init__(self, game: Game):
        super().__init__(game)

        self.name = game.name
        self.date = game.date

        self.odds = {}

        for site in Sites:
            self.odds[site] = game.odds.copy()

class TeamDto(FollowableDto):

    def __init__(self, team: Team):
        super().__init__(team)

        self.name = team.name
        self.current_game = GameDto(team.current_game)




