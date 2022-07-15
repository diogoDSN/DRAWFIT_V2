from __future__ import annotations

from abc import abstractmethod
from typing import List, NoReturn, TYPE_CHECKING

if TYPE_CHECKING:
    from drawfit.domain.domain_store import DomainStore

import discord
from discord.ext import commands

from drawfit.bot.drawfit_bot import DrawfitBot
from drawfit.bot.messages.commands import EmptyArgument
from drawfit.dtos.domain_dto import DomainDto

from drawfit.parameters import COMMAND_CHANNELS

BROWSE_TIMEOUT = 60

def isCommand(ctx: commands.Context) -> bool:

    if ctx.guild:
        for guild in COMMAND_CHANNELS:
            if guild == ctx.guild.name:
                for channel in COMMAND_CHANNELS[guild]:
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

