from bot.DrawfitBot import DrawfitBot
from discord.ext import commands

def isCommand(ctx: commands.Context):

    for guild in DrawfitBot.command_channels:
        if guild == ctx.guild.name:
            for channel in DrawfitBot.command_channels[guild]:
                if channel == ctx.channel.name:
                    return True
            break
    
    return False