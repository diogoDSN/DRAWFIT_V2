from abc import abstractmethod
from datetime import datetime
from typing import Tuple

import drawfit.bot.notify as v
import drawfit.domain.followables as followables

from drawfit.utils import Sites, OddSample


class Notification:

    @abstractmethod
    async def accept(self, visitor: v.Notify):
        pass


class NewOddNotification(Notification):

    def __init__(self, game: followables.Game):
        self.game: followables.Game = game

    
    async def accept(self, visitor: v.Notify):
        await visitor.visitNewOdd(self)
    
    def __eq__(self, o):
        
        if o.__class__ == self.__class__:
            return self.game == o.game
        
        return False
    
    def __str__(self):
        result = f'```{self.game.name} has new odds!\n'

        for site in Sites:
            result += f'{site.name} - {self.game.odds[site.value][-1]}\n'
        
        return result + '```'


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
        await visitor.visitPossibleGame(self)
    
    def __eq__(self, o):
        if o.__class__ == self.__class__:
            return self.followable == o.followable \
               and self.sample == o.sample \
               and self.possible_id == o.possible_id \
               and self.site == o.site
        
        return False

class PossibleGameNotification(PossibleNotification):

    def __init__(self, game: followables.Game, sample: OddSample, site: Sites):
        super().__init__(sample, sample.game_id, site)
        self._game = game
    
    @property
    def followable(self) -> followables.Followable:
        return self._game

    
    def __str__(self):
        return 'PossibleGameNotification'

class PossibleTeamNotification(PossibleNotification):

    def __init__(self, team: followables.Team, sample: OddSample, team_id: Tuple[str], site: Sites):
        super().__init__(sample, team_id, site)
        self._team = team
    
    @property
    def followable(self) -> followables.Followable:
        return self._team

    def __str__(self):
        return 'PossibleTeamNotification'