import asyncio
from discord.ext import commands

from bot.Messages import NoPermission
from bot.converters.NArguments import NArguments
from bot.commands.utils import isCommand

@commands.command()
async def test(ctx: commands.Context, *, arguments: NArguments([]) = ''):

    if not isCommand(ctx):
        return

    if str(ctx.author) != 'Pistache#2173':
        await ctx.send(NoPermission('Nogueira Level'))
    else:
        await ctx.send('This test was successful!')
    
