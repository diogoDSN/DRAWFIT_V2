import asyncio
import traceback

import discord
from discord.ext import commands

from domain.DomainStore import DomainStore
from bot.permissions import Permissions
from updates.UpdateHandler import UpdateHandler



class DrawfitBot(commands.Bot):

    greeting = 'Hello there! - Obi-Wan Kenobi'
    command_channels = {'Vascolândia': ['private-nogueira']}
    
    def __init__(self):

        intents = discord.Intents.default()
        intents.members = True
        super().__init__(command_prefix='$', intents=intents)

        self.store = DomainStore()

        self.permissions = {Permissions.NOGUEIRA: ['Pistache#2173'], Permissions.NORMAL: ['Pistache#2173', 'Periquito#0366', 'Peter Pie#3256']}
        
        self.configureCommands()

    

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

        handler = UpdateHandler(self.store)

        # Run update cycle
        await handler.run()

    async def on_command_error(self, ctx, error):
        if error.__class__ == commands.BadArgument:
            await ctx.send(error)
        elif error.__class__ == commands.CommandNotFound:
            pass
        else:
            raise error

    def configureCommands(self):
        from bot.commands.TestCommand import test
        from bot.commands.AddLeague import addLeague
        from bot.commands.RemoveLeague import removeLeague
        from bot.commands.GetLeagues import getLeagues 

        self.add_command(test)
        self.add_command(addLeague)
        self.add_command(removeLeague)
        self.add_command(getLeagues)