import asyncio
from discord.ext import commands

from bot.messages import NoPermission, EmptyArgument
from bot.commands.utils import isCommand, hasPermission, checkEmptyArguments
from bot.permissions import Permissions

@commands.command()
async def test(ctx: commands.Context, *, arguments = ''):

    if not isCommand(ctx):
        return

    if not hasPermission(ctx, Permissions.NOGUEIRA):
        await ctx.send(NoPermission('Nogueira Level'))
        return
    
    checkEmptyArguments(arguments, 'test')

    await ctx.send('This test was successful!')
    
