from discord.ext import commands

from drawfit.bot.permissions import Permissions
from drawfit.bot.messages import NoPermission
from drawfit.bot.utils import isCommand, hasPermission, checkEmptyArguments

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
    
    