from __future__ import annotations
from typing import List, NoReturn, TYPE_CHECKING

import discord

if TYPE_CHECKING:
    from drawfit.domain.league import League

class DomainDto:

    embed_color = 0xD52E0B
    no_code = 'No Code'

    def makeEmbed(leagues: List[League]) -> discord.Embed:

        embed = discord.Embed(title='Leagues', description='All the leagues currently registered.', color=DomainDto.embed_color)

        for number, league in enumerate(leagues):
            name = f'{number+1}. {league.name}'
            field_value = '```'
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

            embed.add_field(name=name, value=field_value, inline=False)
        
        embed.set_footer(text='Choose number/name of league\nq to quit')

        return embed

    def __init__(self, leagues: List[League]) -> NoReturn:
        self._embed = DomainDto.makeEmbed(leagues)
    
    @property
    def embed(self) -> discord.Embed:
        return self._embed


