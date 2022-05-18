from typing import List

import discord
from discord.ext import commands


from drawfit.bot.permissions import Permissions

def hasPermission(ctx: commands.Context, permission: Permissions) -> bool:
    return str(ctx.author) in ctx.bot.permissions[permission]


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