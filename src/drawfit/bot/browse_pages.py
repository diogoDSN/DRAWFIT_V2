from __future__ import annotations

from abc import abstractmethod
from math import ceil
from datetime import datetime, timedelta, MAXYEAR
from pytz import timezone
from typing import NoReturn, List, Optional, Set


from discord import User, Message, Embed, Reaction

import drawfit.bot.drawfit_bot as bot

from drawfit.dtos.domain_dto import DomainDto
from drawfit.dtos.league_dto import LeagueDto
from drawfit.dtos.followables_dto import FollowableDto, TeamDto, GameDto
from drawfit.dtos.odd_dto import OddDto
from drawfit.utils import Sites, str_dates

from drawfit.parameters import TIME_ZONE

back_emoji = '⬅️'

ids_letter = '*'
keywords_letter = 'k'
considered_letter = 'c'

no_id = 'No Id'
no_considered_ids = 'No Considered Ids'

def addFollowableFields(embed: Embed, followable: FollowableDto, toggle_on: Set[str]) -> NoReturn:
    if ids_letter in toggle_on:
            ids = '```\n'
            for site, id in followable.ids.items():
                ids += f'{site.name:-<10}{id if id is not None else no_id:->40}\n'
            ids += '```'
            embed.add_field(name=f'Ids', value=ids, inline=False)

    if keywords_letter in toggle_on:
        keywords = '`No Keywords`'

        if followable.keywords != []:
            keywords = '```\n'
            for number, keyword in enumerate(followable.keywords):
                keywords += f'{number+1:02}{keyword:->30}\n'
            keywords += '```'

        embed.add_field(name=f'Keywords', value=keywords, inline=False)

    if considered_letter in toggle_on:
        considered = '```\n'
        for site, considered_ids in followable.considered.items():
            considered += f'{site.name}\n'

            if considered_ids == []:
                considered += f'{no_considered_ids:->40}\n'
            else:
                for number, considered_id in enumerate(considered_ids):
                    considered += f'  {number+1:02}{considered_id:->40}\n'
            
        considered += '```'
        embed.add_field(name=f'Considered Ids', value=considered, inline=False)

class Page:

    def __init__(self, user: User, domain: DomainDto, page_message: Message, all_emojis: List[str], toggle_emojis: Set[str], char_toggles: Set[str]) -> NoReturn:
        self.user = user
        self.domain = domain
        self.page_message = page_message

        self.emojis = all_emojis
        self.all_toggles = toggle_emojis

        self.toggles_on = set()
        self.char_toggles = char_toggles
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

        try:
            await self.page_message.edit(content=None, embed=self.makeEmbed())
        except:
            await self.page_message.reply('Error generating page!')

    def isAuthor(self, user: User) -> bool:
        return user == self.user

    async def message(self, message: Message) -> Page:
        
        if not self.isAuthor(message.author):
            return self

        try:

            if message.content in self.char_toggles:
                await message.delete()
                if message.content in self.toggles_on:
                    self.toggles_on.remove(message.content)
                else:
                    self.toggles_on.add(message.content)
                self.change = True
                return self

            number = int(message.content)
            await message.delete()

            return await self.select(number)
        except:
            return self
    
    
    async def addReaction(self, reaction: Reaction, user: User) -> Page:
        if not self.isAuthor(user):
            return self
        
        emoji = str(reaction.emoji)

        if emoji in self.all_toggles and emoji not in self.toggles_on:
            self.toggles_on.add(emoji)
            self.change = True
            return self

        else:
            return await self.buttons(emoji)

    async def removeReaction(self, reaction: Reaction, user: User) -> Page:
        if not self.isAuthor(user):
            return self
        
        emoji = str(reaction.emoji)

        if emoji in self.toggles_on:
            self.toggles_on.remove(emoji)
            self.change = True 
            return self
        else:
            return await self.buttons(emoji)
        
    @abstractmethod
    def makeEmbed(self) -> Embed:
        pass
    
    @abstractmethod
    async def buttons(self, emoji: str) -> Page:
        pass

    @abstractmethod
    async def select(self, number: int) -> Page:
        pass

    


class DomainPage(Page):

    codes_emoji = '*️⃣'
    no_code = 'No Code'
    embed_color = 0xffffff

    def __init__(self, user: User, domain: DomainDto, page_message: Message) -> NoReturn:
        super().__init__(user, domain, page_message, [DomainPage.codes_emoji], {DomainPage.codes_emoji}, set())

    def makeEmbed(self) -> Embed:

        embed = Embed(title='Leagues', description='All the leagues currently registered.', color=DomainPage.embed_color)

        for number, league in enumerate(self.domain.known_leagues):
            name = f'{number+1}. {league.name}'
            
            field_value = '**' + ('Active' if league.active else 'Inactive') + '**'

            if DomainPage.codes_emoji in self.toggles_on:
                field_value += '\n```'
                
                for site, code in league.codes.items():
                    if code != None:
                        field_value += f'{site.name:-<10s}{str(code):->40}\n'
                    else:
                        field_value += f'{site.name:-<10s}{DomainPage.no_code:->40}\n'

                field_value += '```'
            
            embed.add_field(name=name, value=field_value, inline=False)

        
        embed.set_footer(text='Choose league by number.')

        return embed
    
    async def select(self, number: int) -> Page:

        if 0 < number <= len(self.domain.known_leagues): 
            new_page = LeaguePage(self.user, self.domain, self.domain.known_leagues[number-1], self.page_message)
            await new_page.initPage()
            return new_page
        
        return self
    
    async def buttons(self, emoji) -> Page:
        return self


class LeaguePage(Page):

    
    act_teams_emoji = '✅'
    inact_teams_emoji = '❌'
    games_emoji = '⚽'

    def __init__(self, user: User, domain: DomainDto, league: LeagueDto, page_message: Message) -> NoReturn:
        super().__init__(user, domain, page_message, \
                        [back_emoji, LeaguePage.act_teams_emoji, LeaguePage.inact_teams_emoji, LeaguePage.games_emoji], \
                        {LeaguePage.act_teams_emoji, LeaguePage.inact_teams_emoji, LeaguePage.games_emoji}, \
                        set())
        
        self.league = league

        #self.toggles_on = self.toggles_on.union(TeamPage.act_teams_emoji)

    def makeEmbed(self) -> Embed:

        embed = Embed(title=self.league.name, \
                              description=('Active' if self.league.active else 'Inactive'), \
                              color=self.league.color)

        number = 0

        if LeaguePage.act_teams_emoji in self.toggles_on and self.league.followed_teams != []:
            active = '```\n'
            for team in self.league.followed_teams:
                number += 1
                active += f'{number:02}{team.name:->40}\n'
            active += '```'
        
            embed.add_field(name=f'{LeaguePage.act_teams_emoji} - Active Teams', value=active, inline=False)

        if LeaguePage.inact_teams_emoji in self.toggles_on and self.league.inactive_teams != []:
            inactive = '```\n'
            for team in self.league.inactive_teams:
                number += 1
                inactive += f'{number:02}{team.name:->40}\n'
            inactive += '```'
        
            embed.add_field(name=f'{LeaguePage.inact_teams_emoji} - Inactive Teams', value=inactive, inline=False)

        if LeaguePage.games_emoji in self.toggles_on and self.league.current_games != []:
            games = '```\n'
            for game in self.league.current_games:
                number += 1
                games += f'{number:02}{game.name:->40}\n'
            games += '```'

            embed.add_field(name=f'{LeaguePage.games_emoji} - Followed Games', value=games, inline=False)

        embed.set_footer(text='Choose a team/game by number.')

        return embed


    async def buttons(self, emoji) -> Page:

        if emoji == back_emoji:
            new_page = DomainPage(self.user, self.domain, self.page_message)
            await new_page.initPage()
            return new_page

        return self

    async def select(self, number: int) -> Page:
    
        if LeaguePage.act_teams_emoji in self.toggles_on:

            if 0 < number <= len(self.league.followed_teams):
                new_page = TeamPage(self.user, self.domain, self.league, self.league.followed_teams[number-1], self.page_message)
                await new_page.initPage()
                return new_page

            else:
                number -= len(self.league.followed_teams)
        
        if LeaguePage.inact_teams_emoji in self.toggles_on:
            if 0 < number <= len(self.league.inactive_teams):
                new_page = TeamPage(self.user, self.domain, self.league, self.league.inactive_teams[number-1], self.page_message)
                await new_page.initPage()
                return new_page

            else:
                number -= len(self.league.inactive_teams)
        
        if LeaguePage.games_emoji in self.toggles_on:
            if 0 < number <= len(self.league.current_games):
                new_page = GamePage(self.user, self.domain, self.league, self.league.current_games[number-1], self.page_message)
                await new_page.initPage()
                return new_page
        
        return self


class TeamPage(Page):

    game_emoji = '⚽'
    
    def __init__(self, user: User, domain: DomainDto, league: LeagueDto, team: TeamDto, page_message: Message) -> NoReturn:
        super().__init__(user, domain, page_message, \
                    [back_emoji, TeamPage.game_emoji], \
                    set(), \
                    {ids_letter, keywords_letter, considered_letter})
        self.league = league
        self.team = team


    def makeEmbed(self) -> Embed:

        embed = Embed(title=self.team.name, \
                              description=('Active' if self.team.active else 'Inactive'), \
                              color=self.league.color)

        addFollowableFields(embed, self.team, self.toggles_on)
        game = '`No current game.`'

        if self.team.current_game is not None:
            game = '```\n'
            game += f'Name:{self.team.current_game.name:>40}\n'
            game += f'Hours Left:{self.team.current_game.hoursLeft():>34.1f}\n'
            game += '```'
        
        embed.add_field(name='Current Game', value=game, inline=False)

        return embed


    async def buttons(self, emoji) -> Page:

        if emoji == back_emoji:
            new_page = LeaguePage(self.user, self.domain, self.league, self.page_message)
            await new_page.initPage()
            return new_page
        elif emoji == TeamPage.game_emoji and self.team.current_game is not None:
            new_page = GamePage(self.user, self.domain, self.league, self.team.current_game, self.page_message, team=self.team)
            await new_page.initPage()
            return new_page

        return self

    async def select(self, number: int) -> Page:
        return self

class GamePage(Page):

    odds_emoji = '💸'
    no_team = 'Team not found'

    def __init__(self, user: User, domain: DomainDto, league: LeagueDto, game: GameDto, page_message: Message, team: Optional[TeamDto]=None) -> NoReturn:

        emojis = [back_emoji, GamePage.odds_emoji]

        toggle_chars = {ids_letter, keywords_letter, considered_letter}

        super().__init__(user, domain, page_message, emojis, set(), toggle_chars)

        self.league = league
        self.team = team
        self.game = game


    def makeEmbed(self) -> Embed:

        embed = Embed(title=self.game.name, \
                              description=str_dates(self.game.date), \
                              color=self.league.color)

        teams = '```\n'
        teams += f'Team1 {GamePage.no_team if self.game.team1 is None else self.game.team1:>40}\n'
        teams += f'Team2 {GamePage.no_team if self.game.team2 is None else self.game.team2:>40}\n'
        teams += '```'
        embed.add_field(name='Teams', value=teams, inline=False)

        addFollowableFields(embed, self.game, self.toggles_on)

        return embed
    
    async def buttons(self, emoji: str) -> Page:

        new_page = None

        if emoji == back_emoji and self.team is not None:
            new_page = TeamPage(self.user, self.domain, self.league, self.team, self.page_message)

        elif emoji == back_emoji:
            new_page = LeaguePage(self.user, self.domain, self.league, self.page_message)

        elif emoji == GamePage.odds_emoji:
            new_page = OddsHistoryPage(self.user, self.domain, self.league, self.game, self.page_message, self.team)

        if new_page is None:
            return self

        else:
            await new_page.initPage()
            return new_page

    async def select(self, number: int) -> Page:
        return self
    

class OddsHistoryPage(Page):

    next_emoji = '⏭️'
    previous_emoji = '⏮️'
    page_lines = 10

    sites_emojis = {Sites.Bwin :   'bwin',
                    Sites.Betano:  'betano',
                    Sites.Betclic: 'betclic',
                    Sites.Solverde:'solverde',
                    Sites.Moosh:   'moosh',
                    Sites.Betway:  'betway'}

    time = 'time left'
    delta = timedelta(minutes=6) # use timedelta(seconds=bot.DrawfitBot.update_cycle) for the bots update cycle

    def __init__(self, user: User, domain: DomainDto, league: LeagueDto, game: GameDto, page_message: Message, team: Optional[TeamDto]=None) -> NoReturn:
        
        def oddDate(odd: Optional[OddDto]) -> datetime:
            if odd is None:
                tz = timezone(TIME_ZONE)
                return tz.localize(datetime(year=MAXYEAR, month=1, day=1))
            return odd.date

        emojis = [back_emoji, OddsHistoryPage.previous_emoji, OddsHistoryPage.next_emoji]

        toggle_chars = set(OddsHistoryPage.sites_emojis.values())

        super().__init__(user, domain, page_message, emojis, set(), toggle_chars)

        self.league = league
        self.team = team
        self.game = game

        self.toggles_on = self.toggles_on.union(OddsHistoryPage.sites_emojis.values())

        self.page_number = 1
        self.columns = {site: [] for site in Sites}
        self.columns[OddsHistoryPage.time] = []

        lenghts = {site: len(self.game.odds[site])  for site in Sites}
        current_indexes = {site: 0 for site in Sites}

        odds_buffer = {}

        while (current_indexes != lenghts):
                for site in Sites:
                    if current_indexes[site] < len(self.game.odds[site]):
                        odds_buffer[site] = self.game.odds[site][current_indexes[site]]
                    else:
                        odds_buffer[site] = None
                
                min_odd = min(odds_buffer.values(), key=oddDate)

                odds_buffer = {site: odd for site, odd in odds_buffer.items() if min_odd.date - OddsHistoryPage.delta < oddDate(odd) < min_odd.date + OddsHistoryPage.delta}

                self.columns[OddsHistoryPage.time].append(f'{min_odd.hours_left:02.1f}')
                

                for site in Sites:
                    if site in odds_buffer:
                        current_indexes[site] += 1
                        self.columns[site].append(f'{odds_buffer[site].value:1.2f}')
                    else:
                        self.columns[site].append(f'----')
    
    def makeEmbed(self) -> Embed:

        embed = Embed(title=self.game.name, \
                              description=str_dates(self.game.date), \
                              color=self.league.color)

        current_odds = '```\n'

        current_odds += '\nCurrent odds:\n'

        if self.columns[OddsHistoryPage.time] == []:
            last_line = ['This game has no odds.']
        

        else:
            last_line = [self.columns[OddsHistoryPage.time][-1]]

            for _, odd in self.game.odds.items():
                # TODO generate by columns
                if odd == []:
                    last_line.append('----')
                else:
                    last_line.append(f'{odd[-1].value:1.2f}')
            


        current_odds += '|'.join(last_line) + '\n```'

        embed.add_field(name='Current Odds', value=current_odds, inline=False)


        odds_history = '```\n'

        column_labels = ['time']
        for site in self.shownSites:
            column_labels.append(f'{site.small()}')
        
        line = '|'.join(column_labels)
        odds_history += f'{line}\n'
        odds_history += len(line) * '=' + '\n'

        for i in range(self.first_line, self.next_first_line):
            line = [self.columns[OddsHistoryPage.time][i]]

            for site in self.shownSites:
                line.append(f'{self.columns[site][i]:>4}')
            line = '|'.join(line)
            odds_history += f'{line}\n'

        odds_history += '```'
        embed.add_field(name='Odds History', value=odds_history, inline=False)


        return embed
    
    async def buttons(self, emoji: str) -> Page:

        if emoji == back_emoji:
            new_page = GamePage(self.user, self.domain, self.league, self.game, self.page_message, self.team)
            await new_page.initPage()
            return new_page
        elif emoji == OddsHistoryPage.previous_emoji:
            self.page_number = self.page_number - 1 if self.page_number > 1 else self.last_page
            self.change = True
        elif emoji == OddsHistoryPage.next_emoji:
            self.page_number = self.page_number + 1 if self.page_number*OddsHistoryPage.page_lines <= self.total_lines else 1
            self.change = True

        return self


    async def select(self, number: int) -> Page:
        return self

    @property
    def shownSites(self) -> List[Sites]:
        return [site for site in Sites if OddsHistoryPage.sites_emojis[site] in self.toggles_on]
    
    @property
    def last_page(self) -> int:
        return ceil(self.total_lines / OddsHistoryPage.page_lines)
    
    @property
    def first_line(self) -> int:
        return (self.page_number-1)*OddsHistoryPage.page_lines
    
    @property
    def next_first_line(self) -> int:
        return self.page_number*OddsHistoryPage.page_lines if self.page_number*OddsHistoryPage.page_lines < self.total_lines else self.total_lines
    
    @property
    def total_lines(self) -> int:
        return len(self.columns[OddsHistoryPage.time])