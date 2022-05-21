from discord.ext import commands

from drawfit.bot.permissions import Permissions
from drawfit.bot.messages.commands import *
from drawfit.bot.messages import NoPermission
from drawfit.bot.utils import hasPermission
from drawfit.bot.utils.commands import *

from drawfit.utils import BwinCode, BetanoCode, LeagueCodeError


@commands.command()
async def test(ctx: commands.Context, *, arguments = ''):

    if not isCommand(ctx):
        return

    if not hasPermission(ctx, Permissions.NOGUEIRA):
        await ctx.send(NoPermission('Nogueira Level'))
        return
    
    checkEmptyArguments(arguments, 'test')

    await ctx.send('This test was successful!')


# $addLeague (name of new league)
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

# $getLeagues
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

# $removeLeague (name of new league)
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

# $setBwinLeagueCode region_id,competition_id (league_name|league_number)
@commands.command()
async def setBwinLeagueCode(ctx: commands.Context, *, arguments = ''):

    if not isCommand(ctx):
        return

    if not hasPermission(ctx, Permissions.NORMAL):
        await ctx.send(NoPermission(Permissions.NORMAL.value))
        return
    
    args = checkAtLeastNArguments(arguments, 2, setBwinLeagueCodeUsage())

    try:

        code = BwinCode(args[0])
        league = ' '.join(args[1:])

        ctx.bot.store.setLeagueCode(league, code)

        await ctx.send(f'Bwin code: `{args[0]}` added to league `{league}`!')

    except LeagueCodeError as e:
        await ctx.send(e.error_message)

# $setBwinLeagueCode league_id (league_name|league_number)
@commands.command()
async def setBetanoLeagueCode(ctx: commands.Context, *, arguments = ''):

    if not isCommand(ctx):
        return

    if not hasPermission(ctx, Permissions.NORMAL):
        await ctx.send(NoPermission(Permissions.NORMAL.value))
        return
    
    args = checkAtLeastNArguments(arguments, 2, setBwinLeagueCodeUsage())

    try:

        code = BetanoCode(args[0])
        league = ' '.join(args[1:])

        ctx.bot.store.setLeagueCode(league, code)

        await ctx.send(f'Betano code: `{args[0]}` added to league `{league}`!')

    except LeagueCodeError as e:
        await ctx.send(e.error_message)


# $addTeam league_name::team_name
@commands.command()
async def addTeam(ctx: commands.Context, *, arguments = ''):

    if not isCommand(ctx):
        return

    if not hasPermission(ctx, Permissions.NORMAL):
        await ctx.send(NoPermission(Permissions.NORMAL.value))
        return
    
    args = checkNNameArguments(arguments, 2, addTeamUsage())

    if ctx.bot.store.registerTeam(args[0], args[1]):
        await ctx.send(f'New team: `{args[1]}` added!')
    else:
        await ctx.send('Team couldn\'t be added')

# $addTeamKeywords league_name::team_name::keyword1 keyword2 keyword3 ...
@commands.command()
async def addTeamKeywords(ctx: commands.Context, *, arguments = ''):

    if not isCommand(ctx):
        return

    if not hasPermission(ctx, Permissions.NORMAL):
        await ctx.send(NoPermission(Permissions.NORMAL.value))
        return
    
    args = checkNNameArguments(arguments, 3, addTeamKeywordsUsage())

    keywords = args[2].split(' ')

    if '' not in keywords and ctx.bot.store.addTeamKeywords(args[0], args[1], keywords) :
        
        response = f'The following keywords were added to the team `{args[1]}`:\n'

        for keyword in keywords:
            response += f'> {keyword}\n'

        await ctx.send(response)
    else:
        await ctx.send('The given keywords couldn\'t be added')