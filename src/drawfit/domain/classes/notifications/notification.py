from abc import abstractmethod

import drawfit.bot as bot

class Notification:

    @abstractmethod
    async def accept(self, visitor: bot.Notify):
        pass