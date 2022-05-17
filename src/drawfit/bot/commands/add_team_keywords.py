from discord.ext import commands

from drawfit.bot.permissions import Permissions
from drawfit.bot.messages import NoPermission, addTeamUsage
from drawfit.bot.utils import isCommand, hasPermission, checkNNameArguments

# $addTeamKeywords league_name::team_name::keyword1 keyword2 keyword3 ...
@commands.command()
async def addTeamKeywords(ctx: commands.Context, *, arguments = ''):

    if not isCommand(ctx):
        return

    if not hasPermission(ctx, Permissions.NORMAL):
        await ctx.send(NoPermission(Permissions.NORMAL.value))
        return
    
    args = checkNNameArguments(arguments, 3, addTeamUsage())

    keywords = args[2].split(' ')

    if '' not in keywords and ctx.bot.store.addTeamKeywords(args[0], args[1], keywords) :
        
        response = f'The following keywords were added to the team \'{args[1]}\':\n'

        for keyword in keywords:
            response += keyword + '\n'

        await ctx.send(response)
    else:
        await ctx.send('The given keywords couldn\'t be added')
        