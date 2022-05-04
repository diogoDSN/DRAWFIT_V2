from distutils.log import error
from discord.ext import commands

class NArguments(commands.Converter):

    def __init__(self, list_of_converters: list, error_message: str = None):
        self.converters = list_of_converters

        if error_message is None:
            self.message = f'This command has {len(self.converters)} arguments.'
        else:
            self.message = error_message

    async def convert(self, ctx, arguments):

        args = arguments.split(' ')

        if len(args) != len(self.converters) or (len(self.converters) == 0 and arguments != ''):
            raise commands.BadArgument(message=self.message)
        
        if len(self.converters) == 0:
            return []
            
        for index, argument in enumerate(args):
            args[index] = await self.converters[index].convert(ctx, argument)
            
        return args