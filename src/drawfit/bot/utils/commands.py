from typing import List, NoReturn

import discord
from discord.ext import commands

from drawfit.bot.drawfit_bot import DrawfitBot
from drawfit.bot.messages import EmptyArgument

def isCommand(ctx: commands.Context) -> bool:

    for guild in DrawfitBot.command_channels:
        if guild == ctx.guild.name:
            for channel in DrawfitBot.command_channels[guild]:
                if channel == ctx.channel.name:
                    return True
            break
    
    return False


def checkEmptyArguments(arguments: str, command: str) -> NoReturn:
    if arguments != '':
        raise commands.BadArgument(message=EmptyArgument(command))

def checkAnyArguments(arguments: str, message: str) -> NoReturn:
    if arguments == '':
        raise commands.BadArgument(message=message)

def checkNNameArguments(arguments: str, n: int, message: str) -> List[str]:
    args = arguments.split('::')
    if len(args) != n:
        raise commands.BadArgument(message=message)
    
    return args

def checkAtLeastNArguments(arguments: str, n: int, message: str) -> List[str]:
    args = arguments.split(' ')
    if len(args) < n:
        raise commands.BadArgument(message=message)
    return args
