from discord.ext import commands

from bot.messages import NoPermission
from bot.commands.utils import isCommand, hasPermission, checkEmptyArguments
from bot.permissions import Permissions


@commands.command()
async def getLeagues(ctx: commands.Context, *, arguments = ''):

    if not isCommand(ctx):
        return

    if not hasPermission(ctx, Permissions.NORMAL):
        await ctx.send(NoPermission(Permissions.NORMAL.value))
        return
    
    checkEmptyArguments(arguments, 'getLeagues')
    
    leagueDtos = ctx.bot.store.getLeagues()

    answer = 'The known leagues are:\n```'
    if len(leagueDtos) == 0:
        answer += 'No Leagues\n'
    for i, league in enumerate(leagueDtos):
        answer += str(i+1) + ' - '
        if league.active:
            answer += 'A - '
        else:
            answer += 'I - '
        
        answer += league.name + '\n'

    answer += '```A - active, I - inactive'

    await ctx.send(answer)
    
    