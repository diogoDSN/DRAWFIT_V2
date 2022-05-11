from discord.ext import commands

from drawfit.bot.messages import NoPermission, removeLeagueUsage
from drawfit.bot.utils import isCommand, hasPermission, checkAnyArguments
from drawfit.bot import Permissions

@commands.command()
async def removeLeague(ctx: commands.Context, *, arguments = ''):

    if not isCommand(ctx):
        return

    if not hasPermission(ctx, Permissions.NORMAL):
        await ctx.send(NoPermission(Permissions.NORMAL.value))
        return
    
    checkAnyArguments(arguments, removeLeagueUsage())
    
    ctx.drawfit.bot.store.removeLeague(arguments)
    await ctx.send(f'League `{arguments}` removed!')
    
