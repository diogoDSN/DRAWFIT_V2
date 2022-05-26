from __future__ import annotations
from typing import List, NoReturn, TYPE_CHECKING

import discord

if TYPE_CHECKING:
    from drawfit.domain.league import League

class DomainDto:

    embed_color = 0xD52E0B

    def makeEmbed(leagues: List[League]) -> discord.Embed:

        embed = Embed(title='Leagues', description='All the leagues currently registered.', color=DomainDto.embed_color)

        for league in leagues:
            field_value = ''
            if league.active:
                field_value += 'Active\n'
            else:
                field_value += 'Inactive\n'
            
            for code in league.getLeagueCodes():
                field_value += f'{code.getSite().name:-<10s}{str(code):->15s}\n'

            embed.add_field(name=league.name, value=field_value, inline=False)
        
        embed.set_footer(text='Choose number/name of league\nq to quit')

        return embed

    def __init__(self, leagues: List[League]) -> NoReturn:
        self._embed = DomainDto.makeEmbed(leagues)
    
    @property
    def embed(self) -> discord.Embed:
        return self._embed


