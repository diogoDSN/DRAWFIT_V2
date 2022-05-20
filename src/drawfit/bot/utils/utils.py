from typing import List

import discord
from discord.ext import commands

from drawfit.bot.messages import Yes, No
from drawfit.bot.permissions import Permissions

def hasPermission(ctx: commands.Context, permission: Permissions) -> bool:
    return ctx.author in ctx.bot.getUsersWithPermission(permission)


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

    def __init__(self, messages: List[discord.Message], bot: discord.User):
        self.messages = messages
        self.bot = bot
    def check(self, reaction: discord.Reaction, user: discord.User):
        print("Checking for reaction")
        return user != self.bot and reaction.message in self.messages and str(reaction.emoji) in (Yes(), No())