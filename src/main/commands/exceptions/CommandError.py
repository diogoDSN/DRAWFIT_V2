from typing import NoReturn
import discord

class CommandError(Exception):

    def __init__(self, errorMessage: str) -> NoReturn:
        self._errorMessage = errorMessage

    async def reportError(self, channel: discord.TextChannel) -> NoReturn:
        await channel.send(self._errorMessage)