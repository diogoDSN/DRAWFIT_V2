from discord.ext import commands


from drawfit.bot.permissions import Permissions
from drawfit.bot.messages import NoPermission, setBwinLeagueCodeUsage
from drawfit.bot.utils import isCommand, hasPermission, checkAtLeastNArguments

from drawfit.utils import Sites, BwinCode, LeagueCodeError

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
