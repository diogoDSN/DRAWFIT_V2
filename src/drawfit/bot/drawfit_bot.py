import asyncio
import traceback
import time

from typing import List

import discord
from discord.ext import commands

from domain.classes.Sites import Sites
from domain.DomainStore import DomainStore
from drawfit.bot.permissions import Permissions
from updates.UpdateHandler import UpdateHandler
import updates.UpdateHandler as updates


class DrawfitBot(commands.Bot):

    greeting = 'Hello there! - Obi-Wan Kenobi'
    command_channels = {'Vascolândia': ['private-nogueira']}
    
    def __init__(self):

        intents = discord.Intents.default()
        intents.members = True
        super().__init__(command_prefix='.', intents=intents)

        self.store = DomainStore()

        self.permissions = {Permissions.NOGUEIRA: ['Pistache#2173'], \
                            Permissions.MODERATOR: [], \
                            Permissions.NORMAL: ['Periquito#0366', 'Peter Pie#3256']}

        self.update_channels = {}
        for site in Sites:
            self.update_channels[site] = {'Vascolândia' : ['private-nogueira-2']}
        
        self.pending_queries: List[asyncio.Task] = []

        self.configureCommands()
    
    
    def usernamesWithPermission(self, perm: Permissions) -> List[str]:

        usernames = []

        if perm == Permissions.NOGUEIRA:
            usernames += self.permissions[perm]
            perm = Permissions.MODERATOR

        if perm == Permissions.MODERATOR:
            usernames += self.permissions[perm]
            perm = Permissions.NORMAL

        if perm == Permissions().NORMAL:
            usernames += self.permissions[perm]
        
        return usernames

    async def greet(self):
        for guild_name in DrawfitBot.command_channels:
            guild = discord.utils.get(self.guilds, name=guild_name)

            if guild is None:
                continue

            for channel_name in DrawfitBot.command_channels[guild_name]:
                channel = discord.utils.get(guild.text_channels, name=channel_name)

                if channel is None:
                    continue

                await channel.send(DrawfitBot.greeting)    

    async def on_ready(self):

        await self.greet()

        self.handler_routine = asyncio.create_task(self.handlerRoutine())

        await self.handler_routine



    async def on_command_error(self, ctx, error):
        if error.__class__ == commands.BadArgument:
            await ctx.send(error)
        elif error.__class__ == commands.CommandNotFound:
            pass
        else:
            raise error
    

    async def handlerRoutine(self):
        handler = UpdateHandler(self.store)

        print("Reached Update Handler")
        while(True):
            initial_time = time.time()
            print(await handler.update())
            print(f"Time passed: {time.time() - initial_time}")
            await asyncio.sleep(600)


    def configureCommands(self):
        from drawfit.bot.commands import test, addLeague, removeLeague, getLeagues

        self.add_command(test)
        self.add_command(addLeague)
        self.add_command(removeLeague)
        self.add_command(getLeagues)