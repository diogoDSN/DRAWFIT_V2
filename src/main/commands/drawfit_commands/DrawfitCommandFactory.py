from typing import NoReturn
import discord
import re

from commands.Constants import TEST

from commands.drawfit_commands.DrawfitCommand import DrawfitCommand
from commands.drawfit_commands.TestCommand import TestCommand

from commands.exceptions.CommandError import CommandError
from commands.exceptions.CommandErrorMessages import InvalidCommand

from domain.DomainStore import DomainStore

class DrawfitCommandFactory:

    def __init__(self, bot: discord.Client, store: DomainStore) -> NoReturn:
        self._bot = bot
        self._store = store


    def getCommand(self, message: discord.Message, command_str: str) -> DrawfitCommand:

        name, arguments = command_str.split(' ')[0], command_str.split(' ')[1:]
        
        if name == TEST:
            return TestCommand(message, self._bot, arguments)
        else:
            raise CommandError(InvalidCommand())
