import asyncio
from discord.ext import commands

from bot.Messages import NoPermission
from bot.converters.NoArguments import NoArguments
from bot.commands.CommandUtils import isCommand

@commands.command()
async def test(ctx: commands.Context, *, arguments: NoArguments = ''):

    if not isCommand(ctx):
        return

    if str(ctx.author) != 'Pistache#2173':
        await ctx.send(NoPermission('Nogueira Level'))
    else:
        await ctx.send('This test was successful')
    
