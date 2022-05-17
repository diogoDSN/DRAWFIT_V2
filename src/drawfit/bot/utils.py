from typing import List, NoReturn

import discord
from discord.ext import commands


from drawfit.bot import Permissions, DrawfitBot
from drawfit.bot.messages import EmptyArgument

def isCommand(ctx: commands.Context) -> bool:

    for guild in DrawfitBot.command_channels:
        if guild == ctx.guild.name:
            for channel in DrawfitBot.command_channels[guild]:
                if channel == ctx.channel.name:
                    return True
            break
    
    return False


def hasPermission(ctx: commands.Context, permission: Permissions) -> bool:
    return str(ctx.author) in ctx.bot.permissions[permission]


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

class MessageCheck:

    def __init__(self, guild_name, channel_name, author_name):
        self.guild = guild_name
        self.channel = channel_name
        self.author = author_name

    def check(self, msg: discord.Message):
        try:
            return msg.guild.name == self.guild and msg.channel.name == self.channel and str(msg.author) == self.author 
        except AttributeError:
            return False


class ReactionAnswerCheck:

    def __init__(self, messages: List[discord.Message]):
        self.messages = messages
    
    def check(self, reaction: discord.Reaction, user: discord.User):
        return reaction.message in self.messages and reaction.emoji in ("👍", "👎")