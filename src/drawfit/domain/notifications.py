from abc import abstractmethod
from datetime import datetime
from typing import Tuple

import drawfit.bot.notify as v
from drawfit.bot.messages import DateFormating
import drawfit.domain.followables as followables

from drawfit.utils import Sites, OddSample


class Notification:

    @abstractmethod
    async def accept(self, visitor: v.Notify):
        pass


class NewOddNotification(Notification):

    def __init__(self, game: followables.Game):
        self.game: followables.Game = game
        self.creation_time: datetime = datetime.now()

    async def accept(self, visitor: v.Notify):
        await visitor.visitNewOdd(self)
    
    def __eq__(self, o):
        
        if isinstance(o, NewOddNotification):
            return self.game == o.game
        
        return False

    
    def __str__(self):
        result = f'NEW ODDS\n`{self.game.name}`\n{self.creation_time.strftime(DateFormating())}\n'

        for site in Sites:
            if self.game.odds[site] == []:
                odd = "no odds yet"
            else:
                odd = str(self.game.odds[site][-1].value)
            result += f'> {site.name} - {odd}\n'
        
        return result


class PossibleNotification(Notification):

    def __init__(self, sample: OddSample, possible_id: Tuple[str], site: Sites):
        self.sample = sample
        self.possible_id = possible_id
        self.site = site
    
    @property
    @abstractmethod
    def followable(self) -> followables.Followable:
        pass

    async def accept(self, visitor: v.Notify):
        await visitor.visitPossible(self)

class PossibleGameNotification(PossibleNotification):

    def __init__(self, game: followables.Game, sample: OddSample, site: Sites):
        super().__init__(sample, sample.game_id, site)
        self._game = game
    
    @property
    def followable(self) -> followables.Followable:
        return self._game

    def __eq__(self, o):
        if isinstance(o, PossibleGameNotification):
            return self.followable == o.followable \
               and self.sample == o.sample \
               and self.site == o.site
        
        return False
    
    def __str__(self):
        return f'I may have found a match for the game `{game.name}` in the site `{self.site.name}`.\n Does this odd belong to the game you want to track?\n \
                    Name: `{self.sample.game_name}`\n \
                    Date: `{self.sample.start_time}`\n'

class PossibleTeamNotification(PossibleNotification):

    def __init__(self, team: followables.Team, sample: OddSample, team_id: Tuple[str], site: Sites):
        super().__init__(sample, team_id, site)
        self._team = team
    
    @property
    def followable(self) -> followables.Followable:
        return self._team
    
    def __eq__(self, o):
        if isinstance(o, PossibleTeamNotification):
            return self.followable == o.followable \
               and self.sample == o.sample \
               and self.site == o.site
        
        return False

    def __str__(self):
        return f'I may have found a match for the team `{self._team.name}` in the site `{self.site.name}`.\n Does the following team match the team you want to track?\n \
                    Team Name in {self.site.name}: `{self.possible_id[0]}`\n \
                    Game where the name was found: `{self.sample.game_name}`\n'