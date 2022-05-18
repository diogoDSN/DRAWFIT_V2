import asyncio
from typing import NoReturn

import drawfit.bot as bot
import drawfit.domain.classes.notifications as notificaions

from drawfit.bot.permissions import Permissions
from drawfit.bot.utils import ReactionAnswerCheck
from discord.bot.messages import TimedOut, Yes, No

class Notify:

    def __init__(self, bot: bot.DrawfitBot):
        self.bot = bot
        self.channels = bot.getChannels(bot.DrawfitBot.update_channels)
        self.mods = bot.getUsersWithPermissions(Permissions.MODERATOR)
        self.timeout = 86400


    async def visitNewOdd(self, notification: domain.NewOddNotification) -> NoReturn:

        for channel in self.channels:
            await channel.send(notification)

        self.bot.endTask(asyncio.current_task())
    
    async def visitPossible(self, notification: domain.PossibleNotification) -> NoReturn:

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

    