from __future__ import annotations

from typing import TYPE_CHECKING, List, NoReturn

if TYPE_CHECKING:
    from drawfit.bot.drawfit_bot import DrawfitBot

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

    def __init__(self, messages: List[discord.Message], bot: DrawfitBot):
        self.messages = messages
        self.bot = bot
        self.message_ids = [msg.id for msg in messages]
        
    def check(self, payload: discord.RawReactionActionEvent):
        return payload.member     != self.bot.user and \
               payload.message_id in self.message_ids and \
               str(payload.emoji) in (Yes(), No()) and \
               payload.member     in self.bot.getUsersWithPermission(Permissions.MODERATOR)

class ReactionCheck:

    def __init__(self, message: discord.Message, user: discord.User):
        self.message = message
        self._user = user
        
    @property
    def user(self) -> discord.User:
        return self._user

    def check(self, reaction: discord.Reaction, user: discord.User):
        return user == self.user and reaction.message == self.message