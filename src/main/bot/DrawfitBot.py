import asyncio

import discord
from discord.ext import commands

from domain.DomainStore import DomainStore
from updates.UpdateHandler import UpdateHandler



class DrawfitBot(commands.Bot):

    greeting = 'Hello there! - Obi-Wan Kenobi'
    command_channels = {'Vascolândia': ['private-nogueira']}
    
    def __init__(self):

        intents = discord.Intents.default()
        intents.members = True
        super().__init__(command_prefix='$', intents=intents)

        self.store = DomainStore()
        
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
        await ctx.send(error)

    def configureCommands(self):
        from bot.commands.TestCommand import test
        self.add_command(test)