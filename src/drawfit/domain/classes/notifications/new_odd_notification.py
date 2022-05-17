from datetime import datetime

import drawfit.domain as domain
import drawfit.bot as bot

from drawfit.utils import Sites

class NewOddNotification(domain.Notification):

    def __init__(self, game: domain.Game):
        self.game: domain.Game = game

    
    async def accept(self, visitor: bot.Notify):
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
