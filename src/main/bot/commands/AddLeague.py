from asyncio.exceptions import TimeoutError
from discord.ext import commands

from bot.Messages import NoPermission
from bot.converters.NArguments import NArguments
from bot.commands.utils import isCommand, MessageCheck

@commands.command()
async def addLeague(ctx: commands.Context, *, arguments: NArguments([]) = ''):

    if not isCommand(ctx):
        return

    if str(ctx.author) != 'Pistache#2173':
        await ctx.send(NoPermission('Nogueira Level'))
        return
    
    checker = MessageCheck(ctx.guild.name, ctx.channel.name, str(ctx.author))

    await ctx.send('Please give the name of the new league. Example:\n> Itália Série B')
    
    try:
        name = await ctx.bot.wait_for('message', check=checker.check, timeout=10)
        ctx.bot.store.addLeague(name.content)
        await ctx.send(f'New league: `{name.content}` added!')
    except TimeoutError:
        await ctx.send(f'Took to longo to answer. Operation canceled.')
    

