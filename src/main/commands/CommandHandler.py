import asyncio
import re
import discord

from typing import NoReturn

from commands.Constants import COMMAND_KEY, COMMAND_CHANNELS

from commands.exceptions.CommandError import CommandError

from commands.drawfit_commands.DrawfitCommandFactory import DrawfitCommandFactory

from domain.DomainStore import DomainStore


class CommandHandler:
    
    
    def __init__(self, bot: discord.Client, store: DomainStore) -> NoReturn:
        self._bot = bot
        self._commandsBeingHandled = []
        self.greeting = "Hello there! - Obi-Wan Kenobi"
        self._drawfitCommandFactory = DrawfitCommandFactory(bot, store)

    @property
    def store(self) -> DomainStore:
        return self._store
    
    @store.setter
    def store(self, store: DomainStore) -> NoReturn:
        self.store = store

    @property
    def bot(self) -> discord.Client:
        return self._bot
    
    @property
    def commandTasks(self) -> list:
        return self._commandsBeingHandled
    
    @commandTasks.setter
    def commandTasks(self, newList: list) -> NoReturn:
        self._commandsBeingHandled = newList
    
    @property
    def factory(self) -> DrawfitCommandFactory:
        return self._drawfitCommandFactory

    
    async def greet(self):
        for guild_name in COMMAND_CHANNELS:
            guild = discord.utils.get(self.bot.guilds, name=guild_name)

            if guild is None:
                continue

            for channel_name in COMMAND_CHANNELS[guild_name]:
                channel = discord.utils.get(guild.text_channels, name=channel_name)

                if channel is None:
                    continue

                await channel.send(self.greeting)    


    def isCommand(self, message: discord.Message):
        return message.channel.guild.name in COMMAND_CHANNELS \
            and message.channel.name in COMMAND_CHANNELS[message.channel.guild.name] \
            and re.search('\A' + COMMAND_KEY, message.content) is not None


    def addCommandTask(self, task: asyncio.Task) -> NoReturn:
        self._commandsBeingHandled.append(task)


    async def handleCommand(self, message: discord.Message, command_str: str) -> NoReturn:
        try:
            command = self.factory.getCommand(message, command_str)
            await command.execute()
        except CommandError as error:
            await error.reportError(message.channel)
            


    async def run(self) -> NoReturn:

        await self.greet()

        while(True):

            # wait for discord message and add it to the tasks array
            newMessage = await self._bot.wait_for('message')

            # filter commands
            if not self.isCommand(newMessage):
                continue
                
            newTask = asyncio.create_task(self.handleCommand(newMessage, newMessage.content[1:]))
            self.addCommandTask(newTask)
            
            self.commandTasks = list(filter(lambda task: not task.done(), self.commandTasks))


