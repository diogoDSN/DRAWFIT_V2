from sys import path
from os.path import dirname, abspath

path.append(dirname(abspath(__path__)))


import threading
import asyncio

import discord
from updates import UpdateHandler
from commands import CommandHandler



bot = discord.Client()

def handleCommands():
    handler = CommandHandler()
    handler.run()

def handleUpdates():
    handler = UpdateHandler()
    handler.run()


@bot.event
async def on_ready():

    # Create thread to handle discord commands
    commandHandler = threading.Thread(target=handleCommands, name="Thread-1(handleCommands)", daemon=None)
    commandHandler.start()

    # Start update routine
    handleUpdates()

def main():
    TOKEN = ""
    bot.run(TOKEN)


if __name__ == "__main__":
    main()
