from discord.ext import commands

from drawfit.bot.messages import NoPermission, addLeagueUsage
from drawfit.bot.utils import isCommand, hasPermission, checkAnyArguments
from drawfit.bot import Permissions

@commands.command()
async def addLeague(ctx: commands.Context, *, arguments = ''):

    if not isCommand(ctx):
        return

    if not hasPermission(ctx, Permissions.NORMAL):
        await ctx.send(NoPermission(Permissions.NORMAL.value))
        return
    
    checkAnyArguments(arguments, addLeagueUsage())
    
    ctx.bot.store.addLeague(arguments)
    await ctx.send(f'New league: `{arguments}` added!')
    

