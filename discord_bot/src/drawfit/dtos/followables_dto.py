from __future__ import annotations

from typing import TYPE_CHECKING
from datetime import datetime
from drawfit.utils import Sites, now_lisbon


if TYPE_CHECKING:
    from drawfit.domain.followables import Followable, Game, Team

from drawfit.dtos.odd_dto import OddDto


class FollowableDto:

    def __init__(self, followable: Followable):
        self.keywords = {}
        self.considered = {}
        self.ids = {}
        self.complete = followable.complete

        for site in Sites:
            self.keywords = followable.keywords.copy()
            self.ids[site] = ' vs '.join(followable.ids[site]) if followable.ids[site] is not None else 'No Id'
            self.considered[site] = [' vs '.join(id) for id in followable.considered[site]]

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
    
    def hoursLeft(self, time: datetime = None) -> float:

        if self.date is None:
            return 0

        if time is None:
            time = now_lisbon()

        delta = self.date - time
        return delta.total_seconds() / 3600

class TeamDto(FollowableDto):

    def __init__(self, team: Team):
        super().__init__(team)

        self.name = team.name
        self.active = team.active
        self.current_game = None if team.current_game is None else GameDto(team.current_game)




