import asyncio
from discord.ext import commands

from drawfit.bot.messages import NoPermission, EmptyArgument
from drawfit.bot.utils import isCommand, hasPermission, checkEmptyArguments
from drawfit.bot import Permissions

@commands.command()
async def test(ctx: commands.Context, *, arguments = ''):

    if not isCommand(ctx):
        return

    if not hasPermission(ctx, Permissions.NOGUEIRA):
        await ctx.send(NoPermission('Nogueira Level'))
        return
    
    checkEmptyArguments(arguments, 'test')

    await ctx.send('This test was successful!')
    
