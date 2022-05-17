from abc import abstractmethod

from typing import Tuple

import drawfit.bot as bot
import drawfit.domain as domain

from drawfit.utils import Sites, OddSample

class PossibleNotification(domain.Notification):

    def __init__(self, sample: OddSample, possible_id: Tuple[str], site: Sites):
        self.sample = sample
        self.possible_id = possible_id
        self.site = site
    
    @property
    @abstractmethod
    def followable(self) -> domain.Followable:
        pass

    async def accept(self, visitor: bot.Notify):
        await visitor.visitPossibleGame(self)
    
    def __eq__(self, o):
        if o.__class__ == self.__class__:
            return self.followable == o.followable \
               and self.sample == o.sample \
               and self.possible_id == o.possible_id \
               and self.site == o.site
        
        return False