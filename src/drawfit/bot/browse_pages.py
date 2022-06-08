from __future__ import annotations

from abc import abstractmethod
from typing import NoReturn


import discord

from drawfit.dtos.domain_dto import DomainDto


class Page:

    def __init__(self, domain_dto: DomainDto, page_message: discord.Message) -> NoReturn:
        self.domain_dto = domain_dto
        self.page_message = page_message
        self.change = True

    @abstractmethod
    async def addReaction(self, reaction: discord.Reaction, user: discord.User) -> Page:
        pass

    @abstractmethod
    async def removeReaction(self, reaction: discord.Reaction, user: discord.User) -> Page:
        pass

    @abstractmethod
    async def message(self, message: discord.Message) -> Page:
        pass
    
    @abstractmethod
    async def editPage(self) -> NoReturn:
        pass

    @abstractmethod
    async def initPage(self) -> NoReturn:
        pass

    


class DomainPage(Page):

    codes_emoji = '*️⃣'
    no_code = 'No Code'
    embed_color = 0xffffff

    def __init__(self, domain_dto: DomainDto, page_message: discord.Message) -> NoReturn:
        super().__init__(domain_dto, page_message)
        self.show_codes = False
    
    async def initPage(self) -> NoReturn:
        await self.page_message.clear_reactions()
        await self.editPage()
        await self.page_message.add_reaction(DomainPage.codes_emoji)

    async def editPage(self) -> NoReturn:

        if not self.change:
            return
        
        self.change = False

        embed = discord.Embed(title='Leagues', description='All the leagues currently registered.', color=DomainPage.embed_color)

        for number, league in enumerate(self.domain_dto.known_leagues):
            name = f'{number+1}. {league.name}'
            
            field_value = '**' + ('Active' if league.active else 'Inactive') + '**'

            if self.show_codes:
                field_value += '\n```'
                
                for site, code in league.codes.items():
                    if code != None:
                        field_value += f'{site.name:-<10s}{str(code):->30}\n'
                    else:
                        field_value += f'{site.name:-<10s}{DomainPage.no_code:->30}\n'

                field_value += '```'
            
            embed.add_field(name=name, value=field_value, inline=False)

        
        embed.set_footer(text='Choose league by number.')

        await self.page_message.edit(content=None, embed=embed)
    
    async def addReaction(self, reaction: discord.Reaction, user: discord.User) -> Page:
        if str(reaction.emoji) == DomainPage.codes_emoji and self.show_codes == False:
            self.show_codes = True
            self.change = True
        return self
    
    async def removeReaction(self, reaction: discord.Reaction, user: discord.User) -> Page:
        if str(reaction.emoji) == DomainPage.codes_emoji and self.show_codes == True:
            self.show_codes = False
            self.change = True
        return self
    
    async def message(self, message: discord.Message) -> Page:
        try:

            number = int(message.content) - 1

            if self.domain_dto.getLeague(number) is not None:
                new_page = LeaguePage(self.domain_dto, self.page_message, number)
                await new_page.initPage()
                return new_page
            
            return self

        except:
            return self

class LeaguePage(Page):

    back_emoji = '🔙'
    act_teams_emoji = '✅'
    inact_teams_emoji = '❌'
    games_emoji = '⚽'
    not_shown = '*---Not Shown---*'

    def __init__(self, domain_dto: DomainDto, page_message: discord.Message, number: int) -> NoReturn:
        super().__init__(domain_dto, page_message)
        self.league_dto = self.domain_dto.getLeague(number)
        self.active = True
        self.inactive = False
        self.games = False
    
    async def initPage(self) -> NoReturn:
        await self.page_message.clear_reactions()
        await self.editPage()
        await self.page_message.add_reaction(LeaguePage.back_emoji)
        await self.page_message.add_reaction(LeaguePage.act_teams_emoji)
        await self.page_message.add_reaction(LeaguePage.inact_teams_emoji)
        await self.page_message.add_reaction(LeaguePage.games_emoji)

    async def editPage(self) -> NoReturn:

        if not self.change:
            return
        
        self.change = False

        embed = discord.Embed(title=self.league_dto.name, \
                              description=('Active' if self.league_dto.active else 'Inactive'), \
                              color=self.league_dto.color)


        active = LeaguePage.not_shown
        inactive = LeaguePage.not_shown
        games = LeaguePage.not_shown

        number = 0

        if self.active and self.league_dto.followed_teams != []:
            active = '```\n'
            for team in self.league_dto.followed_teams:
                number += 1
                active += f'{number:02}{team.name:->30}\n'
            active += '```'

        if self.inactive and self.league_dto.inactive_teams != []:
            inactive = '```\n'
            for team in self.league_dto.inactive_teams:
                number += 1
                inactive += f'{number:02}{team.name:->30}\n'
            inactive += '```'

        if self.games and self.league_dto.current_games != []:
            games = '```\n'
            for game in self.league_dto.current_games:
                number += 1
                games += f'{number:02}{game.name:->30}\n'
            games += '```'

        embed.add_field(name=f'{LeaguePage.act_teams_emoji} - Active Teams', value=active, inline=False)
        embed.add_field(name=f'{LeaguePage.inact_teams_emoji} - Inactive Teams', value=inactive, inline=False)
        embed.add_field(name=f'{LeaguePage.games_emoji} - Followed Games', value=games, inline=False)

        embed.set_footer(text='Choose a team by number.')

        await self.page_message.edit(content=None, embed=embed)


    async def addReaction(self, reaction: discord.Reaction, user: discord.User) -> Page:
        if str(reaction.emoji) == LeaguePage.act_teams_emoji and not self.active:
            self.active = True
            self.change = True
        elif str(reaction.emoji) == LeaguePage.inact_teams_emoji and not self.inactive:
            self.inactive = True
            self.change = True
        elif str(reaction.emoji) == LeaguePage.games_emoji and not self.games:
            self.games = True
            self.change = True
        elif str(reaction.emoji) == LeaguePage.back_emoji:
            new_page = DomainPage(self.domain_dto, self.page_message)
            await new_page.initPage()
            return new_page

        return self

    async def removeReaction(self, reaction: discord.Reaction, user: discord.User) -> Page:
        if str(reaction.emoji) == LeaguePage.act_teams_emoji and self.active:
            self.active = False
            self.change = True
        elif str(reaction.emoji) == LeaguePage.inact_teams_emoji and self.inactive:
            self.inactive = False
            self.change = True
        elif str(reaction.emoji) == LeaguePage.games_emoji and self.games:
            self.games = False
            self.change = True
        
        return self

    async def message(self, message: discord.Message) -> Page:
        return self
    
