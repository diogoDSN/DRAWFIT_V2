from discord.ext import commands

from bot.messages import NoPermission, removeLeagueUsage
from bot.commands.utils import isCommand, hasPermission, checkAnyArguments
from bot.permissions import Permissions

@commands.command()
async def removeLeague(ctx: commands.Context, *, arguments = ''):

    if not isCommand(ctx):
        return

    if not hasPermission(ctx, Permissions.NORMAL):
        await ctx.send(NoPermission(Permissions.NORMAL.value))
        return
    
    checkAnyArguments(arguments, removeLeagueUsage())
    
    ctx.bot.store.removeLeague(arguments)
    await ctx.send(f'League `{arguments}` removed!')
    
