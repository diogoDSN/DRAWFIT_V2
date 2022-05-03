from discord.ext import commands

class NoArguments(commands.Converter):
    async def convert(self, ctx, arguments):

        if arguments != '':
            raise commands.BadArgument(message='This command has no arguments.')
            
        return arguments