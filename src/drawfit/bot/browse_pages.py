from __future__ import annotations

from abc import abstractmethod
from datetime import datetime, MAXYEAR
from typing import NoReturn, List, Optional


from discord import User, Message, Embed, Reaction

import drawfit.bot.drawfit_bot as bot

from drawfit.dtos.domain_dto import DomainDto
from drawfit.dtos.league_dto import LeagueDto
from drawfit.dtos.followables_dto import FollowableDto, TeamDto, GameDto
from drawfit.dtos.odd_dto import OddDto
from drawfit.utils.sites import Sites

back_emoji = '⬅️'
ids_emoji = '*️⃣'
keywords_emoji = '🇰'
considered_emoji = '🇨'
no_id = 'No Id'
no_considered_ids = 'No Considered Ids'

def addFollowableFields(embed: Embed, followable: FollowableDto, show_ids: bool, show_keywords: bool, show_considered: bool) -> NoReturn:
    if show_ids:
            ids = '```\n'
            for site, id in followable.ids.items():
                ids += f'{site.name:-<10}{(id if id is not None else no_id):->20}\n'
            ids += '```'
            embed.add_field(name=f'{ids_emoji} - Ids', value=ids, inline=False)

    if show_keywords and followable.keywords != []:
        keywords = '```\n'
        for number, keyword in enumerate(followable.keywords):
            keywords += f'{number+1:02}{keyword:->20}\n'
        keywords += '```'
        embed.add_field(name=f'{keywords_emoji} - Keywords', value=keywords, inline=False)

    if show_considered:
        considered = '```\n'
        for site, considered_ids in followable.considered.items():
            considered += f'{site.name}\n'

            if considered_ids == []:
                considered += f'{no_considered_ids:->20}\n'
            else:
                for number, considered_id in enumerate(considered_ids):
                    considered += f'{number+1:02}{considered_id:->18}\n'
            
        considered += '```'
        embed.add_field(name=f'{considered_emoji} - Considered Ids', value=considered, inline=False)

class Page:

    def __init__(self, user: User, domain: DomainDto, page_message: Message, emojis: List[str]) -> NoReturn:
        self.user = user
        self.domain = domain
        self.page_message = page_message
        self.emojis = emojis
        self.change = True

    async def initPage(self) -> NoReturn:
        await self.page_message.clear_reactions()
        await self.editPage()
        
        for emoji in self.emojis:
            await self.page_message.add_reaction(emoji)


    async def editPage(self) -> NoReturn:
        
        if not self.change:
            return
        
        self.change = False

        await self.page_message.edit(content=None, embed=self.makeEmbed())

    def isAuthor(self, user: User) -> bool:
        return user == self.user

    async def message(self, message: Message) -> Page:
        
        if not self.isAuthor(message.author):
            return self

        try:
            number = int(message.content)
            await message.delete()

            return await self.select(number)
        except:
            return self

    @abstractmethod
    def makeEmbed(self) -> Embed:
        pass
    
    @abstractmethod
    async def addReaction(self, reaction: Reaction, user: User) -> Page:
        pass

    @abstractmethod
    async def removeReaction(self, reaction: Reaction, user: User) -> Page:
        pass

    @abstractmethod
    async def select(self, number: int) -> Page:
        pass

    


class DomainPage(Page):

    codes_emoji = '*️⃣'
    no_code = 'No Code'
    embed_color = 0xffffff

    def __init__(self, user: User, domain: DomainDto, page_message: Message) -> NoReturn:
        super().__init__(user, domain, page_message, [DomainPage.codes_emoji])
        self.show_codes = False

    def makeEmbed(self) -> Embed:

        embed = Embed(title='Leagues', description='All the leagues currently registered.', color=DomainPage.embed_color)

        for number, league in enumerate(self.domain.known_leagues):
            name = f'{number+1}. {league.name}'
            
            field_value = '**' + ('Active' if league.active else 'Inactive') + '**'

            if self.show_codes:
                field_value += '\n```'
                
                for site, code in league.codes.items():
                    if code != None:
                        field_value += f'{site.name:-<10s}{str(code):->20}\n'
                    else:
                        field_value += f'{site.name:-<10s}{DomainPage.no_code:->20}\n'

                field_value += '```'
            
            embed.add_field(name=name, value=field_value, inline=False)

        
        embed.set_footer(text='Choose league by number.')

        return embed
    
    async def addReaction(self, reaction: Reaction, user: User) -> Page:

        if not self.isAuthor(user):
            return self

        if str(reaction.emoji) == DomainPage.codes_emoji and self.show_codes == False:
            self.show_codes = True
            self.change = True
        return self
    
    async def removeReaction(self, reaction: Reaction, user: User) -> Page:

        if not self.isAuthor(user):
            return self

        if str(reaction.emoji) == DomainPage.codes_emoji and self.show_codes == True:
            self.show_codes = False
            self.change = True
        return self
    
    async def select(self, number: int) -> Page:

        if 0 < number <= len(self.domain.known_leagues):
            new_page = LeaguePage(self.user, self.domain, self.domain.known_leagues[number-1], self.page_message)
            await new_page.initPage()
            return new_page
        
        return self


class LeaguePage(Page):

    
    act_teams_emoji = '✅'
    inact_teams_emoji = '❌'
    games_emoji = '⚽'

    def __init__(self, user: User, domain: DomainDto, league: LeagueDto, page_message: Message) -> NoReturn:
        super().__init__(user, domain, page_message, [back_emoji, LeaguePage.act_teams_emoji, LeaguePage.inact_teams_emoji, LeaguePage.games_emoji])
        self.league = league
        self.active = True
        self.inactive = False
        self.games = False

    def makeEmbed(self) -> Embed:

        embed = Embed(title=self.league.name, \
                              description=('Active' if self.league.active else 'Inactive'), \
                              color=self.league.color)

        number = 0

        if self.active and self.league.followed_teams != []:
            active = '```\n'
            for team in self.league.followed_teams:
                number += 1
                active += f'{number:02}{team.name:->20}\n'
            active += '```'
        
            embed.add_field(name=f'{LeaguePage.act_teams_emoji} - Active Teams', value=active, inline=False)

        if self.inactive and self.league.inactive_teams != []:
            inactive = '```\n'
            for team in self.league.inactive_teams:
                number += 1
                inactive += f'{number:02}{team.name:->20}\n'
            inactive += '```'
        
            embed.add_field(name=f'{LeaguePage.inact_teams_emoji} - Inactive Teams', value=inactive, inline=False)

        if self.games and self.league.current_games != []:
            games = '```\n'
            for game in self.league.current_games:
                number += 1
                games += f'{number:02}{game.name:->20}\n'
            games += '```'

            embed.add_field(name=f'{LeaguePage.games_emoji} - Followed Games', value=games, inline=False)

        embed.set_footer(text='Choose a team/game by number.')

        return embed


    async def addReaction(self, reaction: Reaction, user: User) -> Page:
        
        if not self.isAuthor(user):
            return self
        
        if str(reaction.emoji) == LeaguePage.act_teams_emoji and not self.active:
            self.active = True
            self.change = True
        elif str(reaction.emoji) == LeaguePage.inact_teams_emoji and not self.inactive:
            self.inactive = True
            self.change = True
        elif str(reaction.emoji) == LeaguePage.games_emoji and not self.games:
            self.games = True
            self.change = True
        elif str(reaction.emoji) == back_emoji:
            new_page = DomainPage(self.user, self.domain, self.page_message)
            await new_page.initPage()
            return new_page

        return self

    async def removeReaction(self, reaction: Reaction, user: User) -> Page:
        
        if not self.isAuthor(user):
            return self
        
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

    async def select(self, number: int) -> Page:
    
        if self.active:
            if 0 < number <= len(self.league.followed_teams):
                new_page = TeamPage(self.user, self.domain, self.league, self.league.followed_teams[number-1], self.page_message)
                await new_page.initPage()
                return new_page

            else:
                number -= len(self.league.followed_teams)
        
        if self.inactive:
            if 0 < number <= len(self.league.inactive_teams):
                new_page = TeamPage(self.user, self.domain, self.league, self.league.inactive_teams[number-1], self.page_message)
                await new_page.initPage()
                return new_page

            else:
                number -= len(self.league.inactive_teams)
        
        if self.games:
            if 0 < number <= len(self.league.current_games):
                new_page = GamePage(self.user, self.domain, self.league, self.league.current_games[number-1], self.page_message)
                await new_page.initPage()
                return new_page
        
        return self


class TeamPage(Page):

    game_emoji = '⚽'
    
    def __init__(self, user: User, domain: DomainDto, league: LeagueDto, team: TeamDto, page_message: Message) -> NoReturn:
        super().__init__(user, domain, page_message, [back_emoji, ids_emoji, keywords_emoji, considered_emoji, TeamPage.game_emoji])
        self.league = league
        self.team = team
        self.show_ids = False
        self.show_keywords = False
        self.show_considered = False

    def makeEmbed(self) -> Embed:

        embed = Embed(title=self.team.name, \
                              description=('Active' if self.team.active else 'Inactive'), \
                              color=self.league.color)

        addFollowableFields(embed, self.team, self.show_ids, self.show_keywords, self.show_considered)
        return embed


    async def addReaction(self, reaction: Reaction, user: User) -> Page:
        if not self.isAuthor(user):
            return self
        

        emoji = str(reaction.emoji)

        if emoji == ids_emoji and not self.show_ids:
            self.show_ids = True
            self.change = True
        elif emoji == keywords_emoji and not self.show_keywords:
            self.show_keywords = True
            self.change = True
        elif emoji == considered_emoji and not self.show_considered:
            self.show_considered = True
            self.change = True
        elif emoji == back_emoji:
            new_page = LeaguePage(self.user, self.domain, self.league, self.page_message)
            await new_page.initPage()
            return new_page
        elif emoji == TeamPage.game_emoji:
            new_page = GamePage(self.user, self.domain, self.league, self.team.current_game, self.page_message, team=self.team)
            await new_page.initPage()
            return new_page

        return self

        

    async def removeReaction(self, reaction: Reaction, user: User) -> Page:
        if not self.isAuthor(user):
            return self
        
        emoji = str(reaction.emoji)

        if emoji == ids_emoji and self.show_ids:
            self.show_ids = False
            self.change = True
        elif emoji == keywords_emoji and self.show_keywords:
            self.show_keywords = False
            self.change = True
        elif emoji == considered_emoji and self.show_considered:
            self.show_considered = False
            self.change = True

        return self

    async def select(self, number: int) -> Page:
        return self

class GamePage(Page):

    odds_emoji = '💸'
    no_team = 'Team not found'

    def __init__(self, user: User, domain: DomainDto, league: LeagueDto, game: GameDto, page_message: Message, team: Optional[TeamDto]=None) -> NoReturn:
        super().__init__(user, domain, page_message, [back_emoji, ids_emoji, keywords_emoji, considered_emoji, GamePage.odds_emoji])
        self.league = league
        self.team = team
        self.game = game

        self.show_ids = False
        self.show_keywords = False
        self.show_considered = False
        self.show_odds = False
        self.small = False
    

    def makeEmbed(self) -> Embed:

        def compareOdds(odd: Optional[OddDto]) -> datetime:
            if odd is not None:
                return odd.date
            return datetime(year=MAXYEAR)

        embed = Embed(title=self.game.name, \
                              description=(self.game.date), \
                              color=self.league.color)

        teams = '```\n'
        teams += f'Team1 {GamePage.no_team if self.game.team1 is None else self.game.team1:>20}\n'
        teams += f'Team2 {GamePage.no_team if self.game.team2 is None else self.game.team2:>20}\n'
        teams += '```'
        embed.add_field(name='Teams', value=teams, inline=False)

        addFollowableFields(embed, self.game, self.show_ids, self.show_keywords, self.show_considered)

        if self.show_odds:
            odds = '```\n'

            line_list = ['date']
            for site in Sites:
                if self.small:
                    line_list.append(f'{site.small():>4}')
                else:
                    line_list.append(f'{site.name:>11}')
            
            line = '|'.join(line_list)
            odds += line
            odds += len(line) * '-'

            lenghts = {site: len(self.game.odds[site])  for site in Sites}
            current_indexes = {site: 0 for site in Sites}

            odds_buffer = {}

            while (current_indexes != lenghts):
                for site in Sites:
                    if current_indexes[site] < len(self.game.odds[site]):
                        odds_buffer[site] = self.game.odds[site][current_indexes[site]]
                    else:
                        odds_buffer[site] = None
                
                min_odd = min(odds_buffer.values(), key=compareOdds)

                odds_buffer = {site: odd for site, odd in odds_buffer.items() if min_odd.date - bot.DrawfitBot.update_cycle < odd.date < min_odd.date + bot.DrawfitBot.update_cycle}

                line_list = []
                for site in Sites:
                    if site in odds_buffer:
                        current_indexes[site] += 1
                        line_list.append(f'{odds_buffer[site].value:1.2f}')

                    
                


            
                


            odds = '```'
            embed.add_field(name='Odds History', value=odds, inline=False)


        return embed
    
    async def addReaction(self, reaction: Reaction, user: User) -> Page:
        if not self.isAuthor(user):
            return self
        
        emoji = str(reaction.emoji)

        if emoji == ids_emoji and not self.show_ids:
            self.show_ids = True
            self.change = True
        elif emoji == keywords_emoji and not self.show_keywords:
            self.show_keywords = True
            self.change = True
        elif emoji == considered_emoji and not self.show_considered:
            self.show_considered = True
            self.change = True
        elif emoji == GamePage.odds_emoji and not self.show_odds:
            self.show_odds = True
            self.change = True
        elif emoji == back_emoji and self.team is not None:
            new_page = TeamPage(self.user, self.domain, self.league, self.team, self.page_message)
            await new_page.initPage()
            return new_page

        return self

    @abstractmethod
    async def removeReaction(self, reaction: Reaction, user: User) -> Page:
        if not self.isAuthor(user):
            return self
        
        emoji = str(reaction.emoji)

        if emoji == ids_emoji and self.show_ids:
            self.show_ids = False
            self.change = True
        elif emoji == keywords_emoji and self.show_keywords:
            self.show_keywords = False
            self.change = True
        elif emoji == considered_emoji and self.show_considered:
            self.show_considered = False
            self.change = True
        elif emoji == GamePage.odds_emoji and self.show_odds:
            self.show_odds = False
            self.change = True

        return self

    @abstractmethod
    async def select(self, number: int) -> Page:
        return self

