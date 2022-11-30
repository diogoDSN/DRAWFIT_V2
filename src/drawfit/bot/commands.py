import asyncio
from re import template
from discord.ext import commands

from drawfit.bot.permissions import Permissions
from drawfit.bot.messages.commands import *
from drawfit.bot.messages import NoPermission, eraseLeagueConfirmation, eraseTeamConfirmation
from drawfit.bot.utils import hasPermission, MessageCheck, ReactionCheck
from drawfit.bot.utils.commands import *
from drawfit.bot.browse_pages import menu, LeaguesPage, TeamsPage, GamesPage

from drawfit.database.drawfit_error import DrawfitError

from drawfit.utils import BwinCode, BetanoCode, SolverdeCode, MooshCode, LeagueCodeError
from drawfit.utils.league_codes.league_codes import BetclicCode, BetwayCode

from drawfit.domain import domain_store as ds


@commands.command(hidden=True)
async def test(ctx: commands.Context, *, arguments = ''):

    if not isCommand(ctx):
        return

    if not hasPermission(ctx, Permissions.OWNER):
        await ctx.send(NoPermission('Owner Level'))
        return
    
    checkEmptyArguments(arguments, 'test')

    await ctx.send('This test was successful!')


@commands.command(aliases=['b', 'browse', 'bl', 'bL', 'Bl', 'BL'])
async def browseLeagues(ctx: commands.Context, *, arguments = ''):

    if not isCommand(ctx):
        return

    if not hasPermission(ctx, Permissions.NORMAL):
        await ctx.send(NoPermission(Permissions.NORMAL.value))
        return
    
    checkEmptyArguments(arguments, 'browse')
    

    browse_message = await ctx.send('*Loading...*')
    domain_dto = ctx.bot.store.getDomain()
    page = LeaguesPage(ctx.author, browse_message, domain_dto.leagues)
    
    await menu(ctx, page, domain_dto)


@commands.command(aliases=['bt', 'bT', 'Bt', 'BT'])
async def browseTeams(ctx: commands.Context, *, arguments = ''):

    if not isCommand(ctx):
        return

    if not hasPermission(ctx, Permissions.NORMAL):
        await ctx.send(NoPermission(Permissions.NORMAL.value))
        return
    
    checkEmptyArguments(arguments, 'browse')
    

    browse_message = await ctx.send('*Loading...*')
    domain_dto = ctx.bot.store.getDomain()
    page = TeamsPage(ctx.author, browse_message, domain_dto.teams)
    
    await menu(ctx, page, domain_dto)

@commands.command(aliases=['bg', 'bG', 'Bg', 'BG'])
async def browseGames(ctx: commands.Context, *, arguments = ''):

    if not isCommand(ctx):
        return

    if not hasPermission(ctx, Permissions.NORMAL):
        await ctx.send(NoPermission(Permissions.NORMAL.value))
        return
    
    checkEmptyArguments(arguments, 'browse')
    

    browse_message = await ctx.send('*Loading...*')
    domain_dto = ctx.bot.store.getDomain()
    page = GamesPage(ctx.author, browse_message, domain_dto.teams)
    
    await menu(ctx, page, domain_dto)


@commands.command(aliases=['aL','al'])
async def addLeague(ctx: commands.Context, *, arguments = ''):

    if not isCommand(ctx):
        return

    if not hasPermission(ctx, Permissions.MODERATOR):
        await ctx.send(NoPermission(Permissions.MODERATOR.value))
        return
    
    checkAnyArguments(arguments, addLeagueUsage())
    
    try:
        ctx.bot.store.registerLeague(arguments)
        await ctx.send(f'New league: `{arguments}` added!')
    except DrawfitError as e:
        await ctx.send(f'League couldn\'t be added.\n{e.error_message}')


# $changeLeagueColor color league_name
@commands.command(aliases=['cLC','color', 'clc'])
async def changeLeagueColor(ctx: commands.Context, *, arguments = ''):

    if not isCommand(ctx):
        return

    if not hasPermission(ctx, Permissions.MODERATOR):
        await ctx.send(NoPermission(Permissions.MODERATOR.value))
        return
    
    checkAnyArguments(arguments, changeLeagueColorCorrectUsage())

    try:

        options = ctx.bot.store.colors_list

        colors = 'Choose from the following colors (use number):\n```'

        for index, color in enumerate(options):
            colors += str(index+1) + ' - ' + color[0] + '\n'

        colors += '```'

        await ctx.send(colors)

        n = -1
        m_check = MessageCheck(ctx)

        while True:

            try:
                message = await ctx.bot.wait_for("message", check=m_check.check, timeout=10)
                n = int(message.content)

                if n < 1 or n > len(options):
                    raise ValueError
                break

            except asyncio.exceptions.TimeoutError:
                await ctx.reply('Timeout')
                return
            except ValueError:
                await message.reply('Invalid color number.')
                continue

        ctx.bot.store.changeLeagueColor(arguments, options[n-1][0])
        await ctx.send('Color successfully changed!')
        
    except DrawfitError as e:
        await ctx.send(f'Color counldn\'t be changed.{e.error_message}')


@commands.command(aliases=['aT', 'at'])
async def addTeam(ctx: commands.Context, *, arguments = ''):

    if not isCommand(ctx):
        return

    if not hasPermission(ctx, Permissions.MODERATOR):
        await ctx.send(NoPermission(Permissions.MODERATOR.value))
        return
    
    checkAnyArguments(arguments, addTeamUsage())

    try:
        ctx.bot.store.registerTeam(arguments)
        await ctx.send(f'New team: `{arguments}` added!')
    except DrawfitError as e:
        await ctx.send(f'Team couldn\'t be added.\n{e.error_message}')


@commands.command(aliases=['bwin'])
async def setBwinLeagueCode(ctx: commands.Context, *, arguments = ''):

    if not isCommand(ctx):
        return

    if not hasPermission(ctx, Permissions.MODERATOR):
        await ctx.send(NoPermission(Permissions.MODERATOR.value))
        return
    
    args = checkAtLeastNArguments(arguments, 2, setBwinLeagueCodeUsage())

    try:

        code = BwinCode(args[0])
        league = ' '.join(args[1:])

        ctx.bot.store.setLeagueCode(league, code)

        await ctx.send(f'Bwin code: `{args[0]}` added to league `{league}`!')

    except LeagueCodeError as e:
        await ctx.send(e.error_message)
    
    except DrawfitError as e:
        await ctx.send(f'Bwin Code coulnd\'t be set.\n{e.error_message}')
        
        
@commands.command(aliases=['betano'])
async def setBetanoLeagueCode(ctx: commands.Context, *, arguments = ''):

    if not isCommand(ctx):
        return

    if not hasPermission(ctx, Permissions.MODERATOR):
        await ctx.send(NoPermission(Permissions.MODERATOR.value))
        return
    
    args = checkAtLeastNArguments(arguments, 2, setBetanoLeagueCodeUsage())

    try:

        code = BetanoCode(args[0])
        league = ' '.join(args[1:])

        ctx.bot.store.setLeagueCode(league, code)

        await ctx.send(f'Betano code: `{args[0]}` added to league `{league}`!')

    except LeagueCodeError as e:
        await ctx.send(e.error_message)
    
    except DrawfitError as e:
        await ctx.send(f'Betano Code coulnd\'t be set.\n{e.error_message}')


@commands.command(aliases=['betclic'])
async def setBetclicLeagueCode(ctx: commands.Context, *, arguments = ''):

    if not isCommand(ctx):
        return

    if not hasPermission(ctx, Permissions.MODERATOR):
        await ctx.send(NoPermission(Permissions.MODERATOR.value))
        return
    
    args = checkAtLeastNArguments(arguments, 2, setBetclicLeagueCodeUsage())

    try:

        code = BetclicCode(args[0])
        league = ' '.join(args[1:])

        ctx.bot.store.setLeagueCode(league, code)

        await ctx.send(f'Betclic code: `{args[0]}` added to league `{league}`!')

    except LeagueCodeError as e:
        await ctx.send(e.error_message)
    
    except DrawfitError as e:
        await ctx.send(f'Betclic Code coulnd\'t be set.\n{e.error_message}')


@commands.command(aliases=['solverde'])
async def setSolverdeLeagueCode(ctx: commands.Context, *, arguments = ''):

    if not isCommand(ctx):
        return

    if not hasPermission(ctx, Permissions.MODERATOR):
        await ctx.send(NoPermission(Permissions.MODERATOR.value))
        return
    
    args = checkAtLeastNArguments(arguments, 2, setSolverdeLeagueCodeUsage())

    try:

        code = SolverdeCode(args[0])
        league = ' '.join(args[1:])

        ctx.bot.store.setLeagueCode(league, code)

        await ctx.send(f'Solverde code: `{args[0]}` added to league `{league}`!')

    except LeagueCodeError as e:
        await ctx.send(e.error_message)
    
    except DrawfitError as e:
        await ctx.send(f'Solverde Code coulnd\'t be set.\n{e.error_message}')


@commands.command(aliases=['moosh'])
async def setMooshLeagueCode(ctx: commands.Context, *, arguments = ''):

    if not isCommand(ctx):
        return

    if not hasPermission(ctx, Permissions.MODERATOR):
        await ctx.send(NoPermission(Permissions.MODERATOR.value))
        return
    
    args = checkNNameArguments(arguments, 2, setMooshLeagueCodeUsage())

    try:

        code = MooshCode(args[0])
        league = args[1]

        ctx.bot.store.setLeagueCode(league, code)

        await ctx.send(f'Moosh code: `{args[0]}` added to league `{league}`!')

    except LeagueCodeError as e:
        await ctx.send(e.error_message)
        
    except DrawfitError as e:
        await ctx.send(f'Moosh Code coulnd\'t be set.\n{e.error_message}')


@commands.command(aliases=['betway'])
async def setBetwayLeagueCode(ctx: commands.Context, *, arguments = ''):

    if not isCommand(ctx):
        return

    if not hasPermission(ctx, Permissions.MODERATOR):
        await ctx.send(NoPermission(Permissions.MODERATOR.value))
        return
    
    args = checkNNameArguments(arguments, 2, setBetwayLeagueCodeUsage())

    try:

        code = BetwayCode(args[0])
        league = args[1]

        ctx.bot.store.setLeagueCode(league, code)

        await ctx.send(f'Betway code: `{args[0]}` added to league `{league}`!')

    except LeagueCodeError as e:
        await ctx.send(e.error_message)
    
    except DrawfitError as e:
        await ctx.send(f'Betway Code coulnd\'t be set.\n{e.error_message}')


@commands.command(aliases=['acT', 'act'])
async def activateTeam(ctx: commands.Context, *, arguments = ''):

    if not isCommand(ctx):
        return

    if not hasPermission(ctx, Permissions.MODERATOR):
        await ctx.send(NoPermission(Permissions.MODERATOR.value))
        return
    
    checkAnyArguments(arguments, activateTeamUsage())
    team_id = arguments

    try: 
        ctx.bot.store.activateTeam(team_id)
        await ctx.send(f'The following team was activated `{team_id}`:\n')
    except DrawfitError as e:
        await ctx.send(f'Team couldn\'t be activated.\n{e.error_message}')


@commands.command(aliases=['dT', 'dt'])
async def deactivateTeam(ctx: commands.Context, *, arguments = ''):

    if not isCommand(ctx):
        return

    if not hasPermission(ctx, Permissions.MODERATOR):
        await ctx.send(NoPermission(Permissions.MODERATOR.value))
        return

    checkAnyArguments(arguments, deactivateTeamUsage())
    team_id = arguments

    try:
        ctx.bot.store.deactivateTeam(team_id)
        await ctx.send(f'The following team was deactivated: `{team_id}`\n')
    except DrawfitError as e:
        await ctx.send(f'Team couldn\'t be deactivated.\n{e.error_message}')


@commands.command(aliases=['aTK', 'atk'])
async def addTeamKeywords(ctx: commands.Context, *, arguments = ''):

    if not isCommand(ctx):
        return

    if not hasPermission(ctx, Permissions.MODERATOR):
        await ctx.send(NoPermission(Permissions.MODERATOR.value))
        return
    
    args = checkNNameArguments(arguments, 2, addTeamKeywordsUsage())

    keywords = args[1].split(' ')

    try:
        ctx.bot.store.addTeamKeywords(args[0], keywords)
        
        response = f'The following keywords were added to the team `{args[0]}`:\n'

        for keyword in keywords:
            response += f'> {keyword}\n'

        await ctx.send(response)
    except DrawfitError as e:
        await ctx.send(f'The given keywords couldn\'t be added.{e.error_message}')



@commands.command(aliases=['eL', 'el'])
async def eraseLeague(ctx: commands.Context, *, league_name = ''):

    if not isCommand(ctx):
        return
    
    if not hasPermission(ctx, Permissions.MODERATOR):
        await ctx.send(NoPermission(Permissions.MODERATOR.value))
        return
    
    checkAnyArguments(league_name, eraseLeagueUsage())

    try:
        
        number_of_games = ctx.bot.store.getTotalLeagueGames(league_name)

        await ctx.send(eraseLeagueConfirmation(league_name, number_of_games))

        m_check = MessageCheck(ctx)
        
        while True:
            try:
                message = await ctx.bot.wait_for("message", check=m_check.check, timeout=10)
                
                if message.content == 'yes':
                    ctx.bot.store.eraseLeague(league_name)
                    await ctx.send(f'The following league and all its games were erased: `{league_name}`\n')
                    return
                elif message.content == 'no':
                    await ctx.send(f'Exiting without erasing the league: `{league_name}`\n')
                    return
                else:
                    raise ValueError()

            except asyncio.exceptions.TimeoutError:
                await ctx.reply('Timeout')
                return
            except ValueError:
                await message.reply('Invalid reply. (yes/no)')
                continue
            
    except DrawfitError as e:
        await ctx.send(f'The given league couldn\'t be erased!\n{e.error_message}')


@commands.command(aliases=['eT', 'et'])
async def eraseTeam(ctx: commands.Context, *, team_name = ''):

    if not isCommand(ctx):
        return
    
    if not hasPermission(ctx, Permissions.MODERATOR):
        await ctx.send(NoPermission(Permissions.MODERATOR.value))
        return
    
    checkAnyArguments(team_name, eraseTeamUsage())

    try:
        
        number_of_games = ctx.bot.store.getTotalTeamGames(team_name)
        await ctx.send(eraseTeamConfirmation(team_name, number_of_games))

        m_check = MessageCheck(ctx)
        
        while True:
            try:
                message = await ctx.bot.wait_for("message", check=m_check.check, timeout=10)
                
                if message.content == 'yes':
                    ctx.bot.store.eraseTeam(team_name)
                    await ctx.send(f'The following team and all its games were erased: `{team_name}`\n')
                    return
                elif message.content == 'no':
                    await ctx.send(f'Exiting without erasing the team: `{team_name}`\n')
                    return
                else:
                    raise ValueError()

            except asyncio.exceptions.TimeoutError:
                await ctx.reply('Timeout')
                return
            except ValueError:
                await message.reply('Invalid reply. (yes/no)')
                continue
            
    except DrawfitError as e:
        await ctx.send(f'The given team couldn\'t be erased!{e.error_message}')


@commands.command(aliases=['rI', 'ri'])
async def resetIds(ctx: commands.Context, *, team_name = ''):

    if not isCommand(ctx):
        return
    
    if not hasPermission(ctx, Permissions.MODERATOR):
        await ctx.send(NoPermission(Permissions.MODERATOR.value))
        return
    
    checkAnyArguments(team_name, resetIdsCorrectUsage())

    try:
        ctx.bot.store.eraseId(team_name)
        await ctx.send(f'The following team had all its ids erased: `{team_name}`')
    except DrawfitError as e:
        await ctx.send(f'The given id couldn\'t be erased!\n{e.error_message}')
