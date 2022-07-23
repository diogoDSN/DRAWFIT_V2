from __future__ import annotations
import asyncio
from asyncio.exceptions import TimeoutError
from typing import NoReturn, TYPE_CHECKING

from discord import Embed

from drawfit.parameters import UPDATES_CHANNELS

if TYPE_CHECKING:
    import drawfit.domain.notifications as notf

import drawfit.bot.drawfit_bot as dbot


from drawfit.bot.permissions import Permissions
from drawfit.bot.utils import ReactionAnswerCheck
from drawfit.bot.messages import TimedOut, Yes, No
from drawfit.parameters import UPDATES_CHANNELS

class Notify:

    def __init__(self, bot: dbot.DrawfitBot):
        self.bot = bot
        self.channels = bot.getChannels(UPDATES_CHANNELS)
        self.mods = bot.getUsersWithPermission(Permissions.MODERATOR)
        self.timeout = 43200

    async def visitNewOdd(self, notification: notf.NewOddNotification) -> NoReturn:

        try:

            embed = Embed(title=notification.game.name, color=notification.color)
            embed.add_field(name=f'Hours Left: {notification.game.hoursLeft():3.1f}', value=str(notification))

            for channel in self.channels:
                await channel.send(embed=embed)
            
        except Exception as e:
            print("Exception raised in visitNewOdd!")
            print(e)
        
        finally:
            self.bot.endTask(asyncio.current_task())

        
    
    async def visitPossible(self, notification: notf.PossibleNotification) -> NoReturn:

        try:

            moderators = self.bot.getUsersWithPermission(Permissions.MODERATOR)

            sent_messages = []

            for moderator in moderators:

                message = await moderator.send(notification)

                await message.add_reaction(Yes())
                await message.add_reaction(No())
                sent_messages.append(message)
            
            answer = ReactionAnswerCheck(sent_messages, self.bot.user)
            reaction, _ = await self.bot.wait_for("reaction_add", check=answer.check, timeout=self.timeout)

            await reaction.message.reply("Answer received.")
            
            if str(reaction.emoji) == Yes():
                notification.followable.setId(notification.site, notification.possible_id)            

        except TimeoutError:

            for msg in sent_messages:
                await msg.reply(TimedOut())
            
            notification.followable.removeConsidered(notification.site, notification.possible_id)
        
        except Exception as e:
            print("Exception raised in visitPossible!")
            print(e)

        finally:
            self.bot.endTask(asyncio.current_task())

    async def visitChangedDate(self, notification: notf.DateChangeNotification) -> NoReturn:

        try:

            embed = Embed(title=notification.game.name, color=notification.color)

            embed.add_field(name='❤️‍🔥Game Date Changed!❤️‍🔥', value=str(notification))

            for channel in self.channels:
                await channel.send(embed=embed)
            
        except Exception as e:
            print("Exception raised in visitNewOdd!")
            print(e)
        
        finally:
            self.bot.endTask(asyncio.current_task())
    