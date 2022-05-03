from typing import NoReturn
from commands.drawfit_commands.DrawfitCommand import DrawfitCommand

import asyncio
import discord
from commands.exceptions.CommandError import CommandError
from commands.exceptions.CommandErrorMessages import NoArguments, NoPermissions

class TestCommand(DrawfitCommand):

    MESSAGE = "This is a test. And it was succesfull!"

    def __init__(self, message: discord.Message, bot: discord.Client, arguments: list) -> NoReturn:
        super().__init__(message, bot, arguments)

    async def execute(self) -> NoReturn:

        if str(self.author) != "Pistache#2173":
            raise CommandError(NoPermissions('Nogueira Level'))

        if len(self.arguments) > 0:
            raise CommandError(NoArguments('test'))
        
        print('BEFORE')
        await self.channel.send(TestCommand.MESSAGE)
        print('AFTER')
        

        
        