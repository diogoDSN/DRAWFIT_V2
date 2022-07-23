from __future__ import annotations

from abc import abstractmethod
from datetime import datetime
from typing import NoReturn, Tuple

import drawfit.bot.notify as v
import drawfit.domain.followables as followables

from drawfit.utils import Sites, OddSample, now_lisbon, str_dates


class Notification:

    @abstractmethod
    async def accept(self, visitor: v.Notify):
        pass


class NewOddNotification(Notification):

    def __init__(self, game: followables.Game, site_updated: Sites, color: int) -> NoReturn:
        self.game: followables.Game = game
        self.creation_time: datetime = now_lisbon()
        self.color: int = color
        self.sites_updated = {site: site == site_updated for site in Sites}

    def mergeNotifications(self, new_notf: Notification) -> NoReturn:
        for site in Sites:
            self.sites_updated[site] = self.sites_updated[site] or new_notf.sites_updated[site]

    async def accept(self, visitor: v.Notify):
        await visitor.visitNewOdd(self)
    
    def __eq__(self, o):
        
        if isinstance(o, NewOddNotification):
            return self.game == o.game
        
        return False

    
    def __str__(self):

        info = '```diff\n'

        for site in Sites:
            if self.game.odds[site] == []:
                odd = 'No Odd'
                info += f'> {site.name:-<10s}{odd:->8}\n'
            else:
                init_symb = '>' if not self.sites_updated[site] else '+' if len(self.game.odds[site]) == 1 or self.game.odds[site][-1].value > self.game.odds[site][-2].value else '-'
                odd = self.game.odds[site][-1].value
                info += f'{init_symb} {site.name:-<10s}{odd:->8.2f}\n'
            
        
        return info + '```'


class PossibleNotification(Notification):

    def __init__(self, sample: OddSample, possible_id: Tuple[str], site: Sites):
        self.sample = sample
        self.possible_id = possible_id
        self.site = site
    
    @property
    @abstractmethod
    def followable(self) -> followables.Followable:
        pass

    def __eq__(self, o) -> bool:
        return False

    async def accept(self, visitor: v.Notify):
        await visitor.visitPossible(self)

class PossibleGameNotification(PossibleNotification):

    def __init__(self, game: followables.Game, sample: OddSample, site: Sites):
        super().__init__(sample, sample.game_id, site)
        self._game = game
    
    @property
    def followable(self) -> followables.Followable:
        return self._game
    
    def __str__(self):
        return f'I may have found a match for the game `{self.game.name}` in the site `{self.site.name}`.\n Does this odd belong to the game you want to track?\n \
                    Name: `{self.sample.game_name}`\n \
                    Date: `{self.sample.start_time}`\n'

class PossibleTeamNotification(PossibleNotification):

    def __init__(self, team: followables.Team, sample: OddSample, team_id: Tuple[str], site: Sites):
        super().__init__(sample, team_id, site)
        self._team = team
    
    @property
    def followable(self) -> followables.Followable:
        return self._team

    def __str__(self) -> str:
        return f'I may have found a match for the team `{self._team.name}` in the site `{self.site.name}`.\n Does the following team match the team you want to track?\n \
                    Team Name in {self.site.name}: `{self.possible_id[0]}`\n \
                    Game where the name was found: `{self.sample.game_name}`\n'
    
    def __repr__(self) -> str:
        return str(self)

class DateChangeNotification(Notification):

    def __init__(self, game: followables.Game, sample: OddSample, color: int):
        self.game = game
        self.sample = sample
        self.color = color
    
    def __eq__(self, o) -> bool:
        if isinstance(o, DateChangeNotification):
            return self.game == o.game

    async def accept(self, visitor: v.Notify):
        await visitor.visitChangedDate(self)
    
    def __str__(self) -> str:
        return f'```\n❗️New Date:❗️\n{str_dates(self.game.date)}\n```'
