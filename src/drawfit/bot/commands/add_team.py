from discord.ext import commands

from drawfit.bot.permissions import Permissions
from drawfit.bot.messages import NoPermission, addTeamUsage
from drawfit.bot.utils import isCommand, hasPermission, checkNNameArguments, MessageCheck

# $addTeam league_name::team_name
@commands.command()
async def addTeam(ctx: commands.Context, *, arguments = ''):

    if not isCommand(ctx):
        return

    if not hasPermission(ctx, Permissions.NORMAL):
        await ctx.send(NoPermission(Permissions.NORMAL.value))
        return
    
    args = checkNNameArguments(arguments, 2, addTeamUsage())

    if ctx.bot.store.addTeam(args[0], args[1]):
        await ctx.send(f'New team: `{arguments}` added!')
    else:
        await ctx.send('Team couldn\'t be added')
