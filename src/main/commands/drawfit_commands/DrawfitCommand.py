from abc import ABC, abstractmethod
from typing import NoReturn
import discord

class DrawfitCommand(ABC):

    def __init__(self, message: discord.Message, bot: discord.Client, arguments: list) -> NoReturn:
        self._message = message
        self._bot = bot
        self._arguments = arguments


    @property
    def msg(self) -> discord.Message:
        return self._message
    
    @property
    def bot(self) -> discord.Client:
        return self._bot

    @property
    def author(self) -> str:
        return self._message.author
    
    @property
    def channel(self) -> discord.TextChannel:
        return self._message.channel
    
    @property
    def arguments(self) -> list:
        return self._arguments
    
    @abstractmethod
    async def execute(self) -> NoReturn:
        pass