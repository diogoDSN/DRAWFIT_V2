from bot.DrawfitBot import DrawfitBot
from discord.ext import commands
import discord

def isCommand(ctx: commands.Context):

    for guild in DrawfitBot.command_channels:
        if guild == ctx.guild.name:
            for channel in DrawfitBot.command_channels[guild]:
                if channel == ctx.channel.name:
                    return True
            break
    
    return False

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
