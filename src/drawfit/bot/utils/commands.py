from __future__ import annotations

from abc import abstractmethod
from typing import List, NoReturn, TYPE_CHECKING

if TYPE_CHECKING:
    from drawfit.domain.domain_store import DomainStore

import discord
from discord.ext import commands

from drawfit.bot.drawfit_bot import DrawfitBot
from drawfit.bot.messages.commands import EmptyArgument
from drawfit.dtos.domain_dto import DomainDto

BROWSE_TIMEOUT = 60

def isCommand(ctx: commands.Context) -> bool:

    if ctx.guild:
        for guild in DrawfitBot.command_channels:
            if guild == ctx.guild.name:
                for channel in DrawfitBot.command_channels[guild]:
                    if channel == ctx.channel.name:
                        return True
                break
    
    return False


def checkEmptyArguments(arguments: str, command: str) -> NoReturn:
    if arguments != '':
        raise commands.BadArgument(message=EmptyArgument(command))

def checkAnyArguments(arguments: str, message: str) -> NoReturn:
    if arguments == '':
        raise commands.BadArgument(message=message)

def checkNNameArguments(arguments: str, n: int, message: str) -> List[str]:
    args = arguments.split('::')
    if len(args) != n:
        raise commands.BadArgument(message=message)
    
    return args

def checkAtLeastNArguments(arguments: str, n: int, message: str) -> List[str]:
    args = arguments.split(' ')
    if len(args) < n:
        raise commands.BadArgument(message=message)
    return args


class Page:

    @abstractmethod
    def addReaction(self) -> Page:
        pass

    @abstractmethod
    def removeReaction(self) -> Page:
        pass

    @abstractmethod
    def message(self) -> Page:
        pass
    
    @abstractmethod
    async def editPage(self) -> discord.Message:
        pass

    


class DomainPage(Page):

    codes_emoji = '*️⃣'

    def __init__(self, domain_dto: DomainDto, page_message: discord.Message) -> NoReturn:
        self.domain_dto = domain_dto
        self.page_message = page_message
        self.show_codes = False
        self.change = True
    
    async def editPage(self) -> discord.Message:

        if self.change == False:
            return
        
        self.change = False

        embed = discord.Embed(title='Leagues', description='All the leagues currently registered.', color=DomainDto.embed_color)

        for number, league in enumerate(self.domain_dto.known_leagues):
            name = f'{number+1}. {league.name}'
            field_value = ''

            if self.show_codes:
                field_value += '```'
                if league.active:
                    name += ' - *Active*'
                else:
                    name += ' - *Inactive*'
                
                for site, code in league.codes.items():
                    if code != None:
                        field_value += f'{site.name:-<10s}{str(code):->30}\n'
                    else:
                        field_value += f'{site.name:-<10s}{DomainDto.no_code:->30}\n'

                field_value += '```'
            else:
                field_value += '*codes not displayed*'

            embed.add_field(name=name, value=field_value, inline=False)
        
        embed.set_footer(text='Choose number/name of league\nq to quit')

        await self.page_message.edit(content=None, embed=embed)
        await self.page_message.add_reaction(DomainPage.codes_emoji)
    
    def addReaction(self, reaction: discord.Reaction, user: discord.User) -> Page:
        if str(reaction.emoji) == DomainPage.codes_emoji and self.show_codes == False:
            self.show_codes = True
            self.change = True
        return self
    
    def removeReaction(self, reaction: discord.Reaction, user: discord.User) -> Page:
        if str(reaction.emoji) == DomainPage.codes_emoji and self.show_codes == True:
            self.show_codes = False
            self.change = True
        return self
    
    def message(self, message: discord.Message) -> Page:
        return self

