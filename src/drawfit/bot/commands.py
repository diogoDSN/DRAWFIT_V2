import asyncio
from re import template
from discord.ext import commands

from drawfit.bot.permissions import Permissions
from drawfit.bot.messages.commands import *
from drawfit.bot.messages import NoPermission
from drawfit.bot.utils import hasPermission, MessageCheck, ReactionCheck
from drawfit.bot.utils.commands import *

from drawfit.utils import BwinCode, BetanoCode, SolverdeCode, MooshCode, LeagueCodeError
from drawfit.utils.league_codes.league_codes import BetclicCode, BetwayCode


@commands.command(hidden=True)
async def test(ctx: commands.Context, *, arguments = ''):

    if not isCommand(ctx):
        return

    if not hasPermission(ctx, Permissions.NOGUEIRA):
        await ctx.send(NoPermission('Nogueira Level'))
        return
    
    checkEmptyArguments(arguments, 'test')

    await ctx.send('This test was successful!')


# $getLeagues
@commands.command(aliases=['b'])
async def browse(ctx: commands.Context, *, arguments = ''):

    if not isCommand(ctx):
        return

    if not hasPermission(ctx, Permissions.NORMAL):
        await ctx.send(NoPermission(Permissions.NORMAL.value))
        return
    
    checkEmptyArguments(arguments, 'browse')
    

    browse_message = await ctx.send('*Loading...*')

    domain_dto = ctx.bot.store.getDomain()
    page = DomainPage(domain_dto, browse_message)

    m_check = MessageCheck(ctx)
    r_check = ReactionCheck(browse_message, ctx.author)


    while True:

        await page.editPage()

        message_task = asyncio.create_task(ctx.bot.wait_for("message", check=m_check.check))
        reaction_add_task = asyncio.create_task(ctx.bot.wait_for("reaction_add", check=r_check.check))
        reaction_remove_task = asyncio.create_task(ctx.bot.wait_for("reaction_remove", check=r_check.check))

        tasks_done, _ = await asyncio.wait([message_task, reaction_add_task, reaction_remove_task], timeout=BROWSE_TIMEOUT, return_when=asyncio.FIRST_COMPLETED)

        if message_task in tasks_done:
            message = await message_task

            if message.content == 'q':
                await browse_message.reply('Exiting')
                break

            page = page.message(message)

        elif reaction_add_task in tasks_done:
            reaction, user = await reaction_add_task
            page = page.addReaction(reaction, user)

        elif reaction_remove_task in tasks_done:
            reaction, user = await reaction_remove_task
            page = page.removeReaction(reaction, user)

        else:
            await browse_message.reply('Exiting')
            break



# $addLeague (name of new league)
@commands.command(aliases=['aL','al'])
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
@commands.command(aliases=['gL','gl'])
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

# $setBwinLeagueCode region_id,competition_id (league_name|league_number)
@commands.command(aliases=['bwin'])
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
@commands.command(aliases=['betano'])
async def setBetanoLeagueCode(ctx: commands.Context, *, arguments = ''):

    if not isCommand(ctx):
        return

    if not hasPermission(ctx, Permissions.NORMAL):
        await ctx.send(NoPermission(Permissions.NORMAL.value))
        return
    
    args = checkAtLeastNArguments(arguments, 2, setBetanoLeagueCodeUsage())

    try:

        code = BetanoCode(args[0])
        league = ' '.join(args[1:])

        ctx.bot.store.setLeagueCode(league, code)

        await ctx.send(f'Betano code: `{args[0]}` added to league `{league}`!')

    except LeagueCodeError as e:
        await ctx.send(e.error_message)


# $setSolverdeLeagueCode country_code,league_id (league_name|league_number)
@commands.command(aliases=['solverde'])
async def setSolverdeLeagueCode(ctx: commands.Context, *, arguments = ''):

    if not isCommand(ctx):
        return

    if not hasPermission(ctx, Permissions.NORMAL):
        await ctx.send(NoPermission(Permissions.NORMAL.value))
        return
    
    args = checkAtLeastNArguments(arguments, 2, setSolverdeLeagueCodeUsage())

    try:

        code = SolverdeCode(args[0])
        league = ' '.join(args[1:])

        ctx.bot.store.setLeagueCode(league, code)

        await ctx.send(f'Solverde code: `{args[0]}` added to league `{league}`!')

    except LeagueCodeError as e:
        await ctx.send(e.error_message)


# $setMooshLeagueCode league_id::(league_name|league_number)
@commands.command(aliases=['moosh'])
async def setMooshLeagueCode(ctx: commands.Context, *, arguments = ''):

    if not isCommand(ctx):
        return

    if not hasPermission(ctx, Permissions.NORMAL):
        await ctx.send(NoPermission(Permissions.NORMAL.value))
        return
    
    args = checkNNameArguments(arguments, 2, setMooshLeagueCodeUsage())

    try:

        code = MooshCode(args[0])
        league = args[1]

        ctx.bot.store.setLeagueCode(league, code)

        await ctx.send(f'Moosh code: `{args[0]}` added to league `{league}`!')

    except LeagueCodeError as e:
        await ctx.send(e.error_message)

# $setBetwayLeagueCode league_id::(league_name|league_number)
@commands.command(aliases=['betway'])
async def setBetwayLeagueCode(ctx: commands.Context, *, arguments = ''):

    if not isCommand(ctx):
        return

    if not hasPermission(ctx, Permissions.NORMAL):
        await ctx.send(NoPermission(Permissions.NORMAL.value))
        return
    
    args = checkNNameArguments(arguments, 2, setBetwayLeagueCodeUsage())

    try:

        code = BetwayCode(args[0])
        league = args[1]

        ctx.bot.store.setLeagueCode(league, code)

        await ctx.send(f'Betway code: `{args[0]}` added to league `{league}`!')

    except LeagueCodeError as e:
        await ctx.send(e.error_message)

# $setBwinLeagueCode league_id (league_name|league_number)
@commands.command(aliases=['betclic'])
async def setBetclicLeagueCode(ctx: commands.Context, *, arguments = ''):

    if not isCommand(ctx):
        return

    if not hasPermission(ctx, Permissions.NORMAL):
        await ctx.send(NoPermission(Permissions.NORMAL.value))
        return
    
    args = checkAtLeastNArguments(arguments, 2, setBetclicLeagueCodeUsage())

    try:

        code = BetclicCode(args[0])
        league = ' '.join(args[1:])

        ctx.bot.store.setLeagueCode(league, code)

        await ctx.send(f'Betclic code: `{args[0]}` added to league `{league}`!')

    except LeagueCodeError as e:
        await ctx.send(e.error_message)



# $addTeam league_name::team_name
@commands.command(aliases=['aT'])
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
@commands.command(aliases=['aTK'])
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


# $addTeamKeywords league_name::team_name
@commands.command(aliases=['acT', 'act'])
async def activateTeam(ctx: commands.Context, *, arguments = ''):

    if not isCommand(ctx):
        return

    if not hasPermission(ctx, Permissions.NORMAL):
        await ctx.send(NoPermission(Permissions.NORMAL.value))
        return
    
    args = checkNNameArguments(arguments, 2, addTeamKeywordsUsage())

    league_id, team_id = args

    if ctx.bot.store.activateTeam(league_id, team_id):
        
        response = f'The following team was activated `{team_id}`:\n'
        await ctx.send(response)
    else:
        await ctx.send('The given team couldn\'t be activated')

# $addTeamKeywords league_name::team_name
@commands.command(aliases=['dT', 'dt'])
async def deactivateTeam(ctx: commands.Context, *, arguments = ''):

    if not isCommand(ctx):
        return

    if not hasPermission(ctx, Permissions.NORMAL):
        await ctx.send(NoPermission(Permissions.NORMAL.value))
        return

    args = checkNNameArguments(arguments, 2, addTeamKeywordsUsage())

    league_id, team_id = args

    if ctx.bot.store.deactivateTeam(league_id, team_id):
        
        response = f'The following team was deactivated `{team_id}`:\n'
        await ctx.send(response)
    else:
        await ctx.send('The given team couldn\'t be deactivated')

@commands.command(aliases=['s'])
async def save(ctx: commands.Context, *, arguments = ''):

    if not isCommand(ctx):
        return

    if not hasPermission(ctx, Permissions.MODERATOR):
        await ctx.send(NoPermission(Permissions.MODERATOR.value))
        return
    
    checkEmptyArguments(arguments, 'save')

    if ctx.bot.save():
        await ctx.send('Save successful')
    else:
        await ctx.send('**An error occurred! Couldn\'t save.**')