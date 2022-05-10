from discord.ext import commands

from bot.messages import NoPermission, addLeagueUsage
from bot.commands.utils import isCommand, hasPermission, checkAnyArguments
from bot.permissions import Permissions

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
    

