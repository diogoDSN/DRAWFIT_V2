from __future__ import annotations
import asyncio
from typing import NoReturn, TYPE_CHECKING

if TYPE_CHECKING:
    import drawfit.domain.notifications as notf

import drawfit.bot.drawfit_bot as dbot


from drawfit.bot.permissions import Permissions
from drawfit.bot.utils import ReactionAnswerCheck
from drawfit.bot.messages import TimedOut, Yes, No

class Notify:

    def __init__(self, bot: dbot.DrawfitBot):
        self.bot = bot
        self.channels = bot.getChannels(dbot.DrawfitBot.update_channels)
        self.mods = bot.getUsersWithPermission(Permissions.MODERATOR)
        self.timeout = 86400


    async def visitNewOdd(self, notification: notf.NewOddNotification) -> NoReturn:

        for channel in self.channels:
            await channel.send(notification)

        self.bot.endTask(asyncio.current_task())
    
    async def visitPossible(self, notification: notf.PossibleNotification) -> NoReturn:

        notification.followable.addConsidered(notication.site, notification.possible_id)

        moderators = self.bot.getUsersWithPermission(Permissions.MODERATOR)

        sent_messages = []

        for moderator in moderators:

            message = await moderator.send(notification)

            await message.add_reaction(Yes())
            await message.add_reaction(No())
            sent_messages.append(message)
        
        answer = ReactionAnswerCheck(sent_messages)
            
        try:
            reaction, _ = await self.bot.wait_for("on_reaction_add", check=answer.check, timeout=self.timeout)

            await reaction.message.reply("Answer received.")
            
            if reaction.emoji == Yes():
                notification.followable.setId(notification.site, notification.possible_id)            

        except TimeoutError:

            for msg in sent_messages:
                msg.reply(TimedOut())
            
            notification.followable.removeConsidered(notification.site, notification.possible_id)
        
        finally:
            self.bot.endTask(asyncio.current_task())

    