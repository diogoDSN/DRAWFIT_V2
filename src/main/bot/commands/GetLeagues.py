from discord.ext import commands

from bot.Messages import NoPermission
from bot.converters.NArguments import NArguments
from bot.commands.utils import isCommand

@commands.command()
async def getLeagues(ctx: commands.Context, *, arguments: NArguments([]) = ''):

    if not isCommand(ctx):
        return

    if str(ctx.author) != 'Pistache#2173':
        await ctx.send(NoPermission('Nogueira Level'))
        return
    
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
    
    