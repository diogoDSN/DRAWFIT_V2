import sys
from os.path import dirname, abspath

sys.path.append(dirname(abspath(__file__)))

import asyncio
import discord
from updates.UpdateHandler import UpdateHandler
from commands.CommandHandler import CommandHandler
from domain.DomainStore import DomainStore


bot = discord.Client()


async def handleCommands(bot, store):
    handler = CommandHandler(bot, store)
    await handler.run()

async def handleUpdates():
    handler = UpdateHandler()
    await handler.run()



@bot.event
async def on_ready():

    # Create DomainStore
    store = DomainStore()

    # Gather tasks to run the bot
    await asyncio.gather(handleCommands(bot, store), handleUpdates())

def main():
    TOKEN = "OTUxOTEzMzQzNDk1NTY5NDY4.YiuYYg.gCo2OSLi-u86EWGY47yY9MkmdB0"
    bot.run(TOKEN)


if __name__ == "__main__":
    main()
