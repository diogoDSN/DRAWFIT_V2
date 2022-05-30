from typing import List, NoReturn

import discord
from discord.ext import commands

from drawfit.bot.messages import Yes, No
from drawfit.bot.permissions import Permissions

def hasPermission(ctx: commands.Context, permission: Permissions) -> bool:
    return ctx.author in ctx.bot.getUsersWithPermission(permission)


class MessageCheck:

    def __init__(self, ctx):
        self.ctx = ctx

    def check(self, msg: discord.Message):
        try:
            return msg.guild == self.ctx.guild and msg.channel == self.ctx.channel and msg.author == self.ctx.author 
        except AttributeError:
            return False


class ReactionAnswerCheck:

    def __init__(self, messages: List[discord.Message], bot: discord.User):
        self.messages = messages
        self.bot = bot
        
    def check(self, reaction: discord.Reaction, user: discord.User):
        return user != self.bot and reaction.message in self.messages and str(reaction.emoji) in (Yes(), No())

class ReactionCheck:

    def __init__(self, message: discord.Message, user: discord.User):
        self.message = message
        self._user = user
        
    @property
    def user(self) -> discord.User:
        return self._user

    def check(self, reaction: discord.Reaction, user: discord.User):
        return user == self.user and reaction.message == self.message