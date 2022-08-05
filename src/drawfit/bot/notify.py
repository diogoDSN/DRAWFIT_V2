from __future__ import annotations
import asyncio
from asyncio.exceptions import TimeoutError
from typing import NoReturn, TYPE_CHECKING

from discord import Embed

from drawfit.parameters import QUERIES_CHANNELS, UPDATES_CHANNELS

if TYPE_CHECKING:
    import drawfit.domain.notifications as notf

import drawfit.bot.drawfit_bot as dbot


from drawfit.bot.permissions import Permissions
from drawfit.bot.utils import ReactionAnswerCheck
from drawfit.bot.messages import TimedOut, Yes, No
from drawfit.parameters import UPDATES_CHANNELS, QUERIES_CHANNELS

class Notify:

    def __init__(self, bot: dbot.DrawfitBot):
        self.bot = bot
        self.updates_channels = bot.getChannels(UPDATES_CHANNELS)
        self.queries_channels = bot.getChannels(QUERIES_CHANNELS)
        self.mods = bot.getUsersWithPermission(Permissions.MODERATOR)
        self.timeout = 60

    async def visitNewOdd(self, notification: notf.NewOddNotification) -> NoReturn:

        try:

            embed = Embed(title=notification.game.name, color=notification.color)
            embed.add_field(name=f'Hours Left: {notification.game.hoursLeft():3.1f}', value=str(notification))

            for channel in self.updates_channels:
                await channel.send(embed=embed)
            
        except Exception as e:
            print("Exception raised in visitNewOdd!")
            print(e)
        
        finally:
            self.bot.endTask(asyncio.current_task())

        
    
    async def visitPossible(self, notification: notf.PossibleNotification) -> NoReturn:

        try:

            sent_messages = []

            #TODO embed creation for notification
            embed = Embed(title=notification.followable.name, color=notification.color)
            embed.add_field(name=f'Name found for `{notification.site.name}`', value=str(notification))

            for channel in self.queries_channels:

                msg = await channel.send(embed=embed)

                await msg.add_reaction(Yes())
                await msg.add_reaction(No())
                sent_messages.append(msg)
            
            answer = ReactionAnswerCheck(sent_messages, self.bot)
            payload = await self.bot.wait_for("raw_reaction_add", check=answer.check, timeout=self.timeout)

            for msg in sent_messages:
                await msg.delete()
            
            if str(payload.emoji) == Yes():
                notification.followable.setId(notification.site, notification.possible_id)            

        except TimeoutError:

            for msg in sent_messages:
                await msg.reply(TimedOut())
            
            print('TimedOut')
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

            for channel in self.updates_channels:
                await channel.send(embed=embed)
            
        except Exception as e:
            print("Exception raised in visitNewOdd!")
            print(e)
        
        finally:
            self.bot.endTask(asyncio.current_task())
    