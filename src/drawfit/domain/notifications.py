from __future__ import annotations

from abc import abstractmethod
from datetime import datetime
from typing import NoReturn, Tuple

import drawfit.bot.notify as v
import drawfit.domain.followables as followables
import drawfit.database.database_store as d

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
                init_symb, last_symb = ('>', '') if not self.sites_updated[site] else ('+', '🟢') if len(self.game.odds[site]) == 1 or self.game.odds[site][-1].value > self.game.odds[site][-2].value else ('-', '🔴')
                odd = self.game.odds[site][-1].value
                info += f'{init_symb} {site.name:-<10s}{odd:->8.2f} {last_symb}\n'
            
        
        return info + '```'
    

class PossibleTeamNotification(Notification):

    def __init__(self, team: followables.Team, sample: OddSample, team_id: Tuple[str], site: Sites, color: int, db_store: d.DatabaseStore):
        self.db_store = db_store
        self.team = team
        self.sample = sample
        self.possible_id = team_id
        self.site = site
        self.color = color
    
    def registerId(self) -> NoReturn:
        with self.db_store as db:
            db.addTeamId(self.team.name, self.site, self.possible_id)
        self.team.setId(self.site, self.possible_id)
    
    def removeConsidered(self) -> NoReturn:
        self.team.removeConsidered(self.site, self.possible_id)
    
    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, o) -> bool:
        return False
    
    def __str__(self):
        return '> ' + ' vs '.join(self.possible_id)

    async def accept(self, visitor: v.Notify):
        await visitor.visitPossibleTeam(self)

class DateChangeNotification(Notification):

    def __init__(self, game: followables.Game, sample: OddSample, color: int):
        self.game = game
        self.sample = sample
        self.color = color
    
    def __eq__(self, o) -> bool:
        if isinstance(o, DateChangeNotification):
            return self.game == o.game

    def mergeNotifications(self, new_notf: Notification) -> NoReturn:
        pass

    async def accept(self, visitor: v.Notify):
        await visitor.visitChangedDate(self)
    
    def __str__(self) -> str:
        return f'```\n❗️New Date:❗️\n{str_dates(self.game.date)}\n```'
