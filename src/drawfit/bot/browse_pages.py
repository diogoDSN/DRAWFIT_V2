from __future__ import annotations

from abc import abstractmethod
import traceback
from math import ceil
from datetime import datetime, timedelta, MAXYEAR
from pytz import timezone
from typing import NoReturn, List, Optional, Set, Union, Dict
import asyncio


from discord import User, Message, Embed, Reaction
from discord.ext import commands

import drawfit.bot.drawfit_bot as bot
from drawfit.bot.utils import MessageCheck, ReactionCheck
from drawfit.bot.permissions import Permissions

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

BROWSE_TIMEOUT = 60

async def menu(ctx: commands.Context, page: Page, domain: DomainDto) -> NoReturn:

    m_check = MessageCheck(ctx)
    r_check = ReactionCheck(page.page_message, ctx.author)

    await page.initPage()

    while True:

        message_task = asyncio.create_task(ctx.bot.wait_for("message", check=m_check.check))
        reaction_add_task = asyncio.create_task(ctx.bot.wait_for("reaction_add", check=r_check.check))
        reaction_remove_task = asyncio.create_task(ctx.bot.wait_for("reaction_remove", check=r_check.check))

        tasks_done, _ = await asyncio.wait([message_task, reaction_add_task, reaction_remove_task], timeout=BROWSE_TIMEOUT, return_when=asyncio.FIRST_COMPLETED)

        if message_task in tasks_done:
            message = await message_task

            if not page.isAuthor(message.author):
                continue
    
            if message.content == 'q':
                await page.page_message.reply('Exiting')
                break
            if message.content == 'l':
                page = LeaguesPage(page.user, page.page_message, domain.leagues)
            elif message.content == 't':
                page = TeamsPage(page.user, page.page_message, domain.teams)
            elif message.content == 'g':
                page = GamesPage(page.user, page.page_message, domain.teams)
            
            if message.content in ['l', 't', 'g']:
                await message.delete()
                await page.initPage()
            else:
                page = await page.message(message)
            

        elif reaction_add_task in tasks_done:
            reaction, user = await reaction_add_task
            page = await page.addReaction(reaction, user)

        elif reaction_remove_task in tasks_done:
            reaction, user = await reaction_remove_task
            page = await page.removeReaction(reaction, user)

        else:
            await page.page_message.reply('Exiting')
            break

        await page.editPage()


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

def createOddsTable(odds_dict: Dict[site, List[str]], times_list: List[str], sites_order: List[site]) -> str:
    
    # Create column labels
    labels_list = ['time ']
    for site in sites_order:
        labels_list.append(f'{site.small()}')

    line = '|'.join(labels_list) + '\n'
    column_labels = line + (len(line)-1) * '=' + '\n'
    

    # Create odds table
    odds_table = '```\n' + column_labels

    for i, time in enumerate(times_list):
        line = [time]
        line.extend([f'{odds_dict[site][i]:>4}' for site in sites_order])
        
        line = '|'.join(line)
        odds_table += f'{line}\n'

    return odds_table + '```'

class Page:

    def __init__(self, user: User, page_message: Message, all_emojis: List[str], toggle_emojis: Set[str], char_toggles: Set[str]) -> NoReturn:
        self.user = user
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
        except ValueError:
            pass
        except Exception:
            print(traceback.format_exc())
            await self.page_message.reply('Error generating page!')

    def isAuthor(self, user: User) -> bool:
        return user == self.user

    async def message(self, message: Message) -> Page:
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
        except Exception:
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

class SubPagedPage(Page):
    next_emoji = '⏭️'
    previous_emoji = '⏮️'
    
    def __init__(self, user: User, page_message: Message, all_emojis: List[str], toggle_emojis: Set[str], char_toggles: Set[str], page_size: int, number_of_items: int) -> NoReturn:
        emojis = [SubPagedPage.previous_emoji, SubPagedPage.next_emoji]
        emojis.extend(all_emojis)
        super().__init__(user, page_message, emojis, toggle_emojis, char_toggles)
        self.page_number = 1
        self.page_size = page_size
        self.number_of_items = number_of_items
    
    @property
    def total_pages(self) -> int:
        return ceil(self.number_of_items / self.page_size)
    
    @property
    def first_page_item(self) -> int:
        return (self.page_number-1) * self.page_size
    
    @property
    def last_page_item(self) -> int:
        return (self.page_number) * self.page_size
    
    def next_page(self):
        self.change = True
        self.page_number = self.page_number + 1 if self.page_number < self.total_pages else 1
    
    def prevoius_page(self):
        self.change = True
        self.page_number = self.page_number - 1 if self.page_number > 1 else self.total_pages
    


class LeaguesPage(SubPagedPage):

    codes = '*'
    no_code = 'No Code'
    page_size = 10
    embed_color = 0xffffff

    def __init__(self, user: User, page_message: Message, leagues: List[LeagueDto]) -> NoReturn:
        super().__init__(user, page_message, \
            [LeaguesPage.next_emoji, LeaguesPage.previous_emoji], \
            set(), \
            {LeaguesPage.codes}, \
            LeaguesPage.page_size, \
            len(leagues) \
        )
        self.leagues = leagues

    def makeEmbed(self) -> Embed:

        embed = Embed(title='Leagues', description=f'({self.page_number}/{self.total_pages})', color=LeaguesPage.embed_color)
        
        for i, league in list(enumerate(self.leagues))[self.first_page_item:self.last_page_item]:
            name = f'**{i+1}. {league.name}**'
            field_value = f'{len([team for team in league.teams if not team.current_game is None and team.current_game.league is league])} current games.'

            if LeaguesPage.codes in self.toggles_on:
                field_value += '\n```'
                
                for site, code in league.codes.items():
                    if code != None:
                        field_value += f'{site.name:-<10s}{str(code):->40}\n'
                    else:
                        field_value += f'{site.name:-<10s}{LeaguesPage.no_code:->40}\n'

                field_value += '```'
            
            embed.add_field(name=name, value=field_value, inline=False)

        embed.set_footer(text='Choose league by number.')

        return embed
    
    async def select(self, number: int) -> Page:

        if 0 < number <= len(self.leagues):
            new_page = LeaguePage(self.user, self.leagues[number-1], self.page_message)
            await new_page.initPage()
            return new_page
        
        return self
    
    async def buttons(self, emoji) -> Page:
        if emoji == SubPagedPage.next_emoji:
            self.next_page()
        elif emoji == SubPagedPage.previous_emoji:
            self.prevoius_page()
        return self
            
class TeamsPage(SubPagedPage):

    page_size = 10
    embed_color = 0xffffff

    def __init__(self, user: User, page_message: Message, teams: List[TeamDto]) -> NoReturn:
        super().__init__(user, page_message, \
            [LeaguesPage.next_emoji, LeaguesPage.previous_emoji], \
            {}, \
            set(), \
            TeamsPage.page_size, \
            len(teams) \
        )
        self.teams = teams

    def makeEmbed(self) -> Embed:

        embed = Embed(title='Teams', description=f'({self.page_number}/{self.total_pages})', color=TeamsPage.embed_color)
        
        for i, team in list(enumerate(self.teams))[self.first_page_item:self.last_page_item]:
            name = f'**{i+1}. {team.name}**'

            field_value = f'{LeaguePage.active_emoji if team.active else LeaguePage.inactive_emoji}\n'
            
            if team.current_game is None:
                field_value += f'No current game.'
            else:
                field_value += team.current_game.name
                            
            embed.add_field(name=name, value=field_value, inline=False)

        embed.set_footer(text='Choose team by number.')

        return embed
    
    async def select(self, number: int) -> Page:

        if 0 < number <= len(self.teams):
            new_page = TeamPage(self.user, self.teams[number-1], self.page_message)
            await new_page.initPage()
            return new_page
        
        return self
    
    async def buttons(self, emoji) -> Page:
        if emoji == SubPagedPage.next_emoji:
            self.next_page()
        elif emoji == SubPagedPage.previous_emoji:
            self.prevoius_page()
        return self
    

class GamesPage(SubPagedPage):
    
    page_size = 1
    
    def __init__(self, user, page_message, teams: List[TeamDto]):
        self.games = [team.current_game for team in teams if not team.current_game is None]
        self.games.sort(key= lambda game: game.hoursLeft())
        
        super().__init__(user, page_message, [GamePage.team_emoji, GamePage.league_emoji, GamePage.odds_emoji], set(), set(), GamesPage.page_size, len(self.games))
        
        self.prev_page_number = self.page_number
        self._current_page = GamePage(self.user, self.games[self.page_number-1], self.page_message)
    
    @property
    def current_page(self) -> GamesPage:
        if self.prev_page_number != self.page_number:
            self._current_page = GamePage(self.user, self.games[self.page_number-1], self.page_message) 
            self.prev_page_number = self.page_number
            
        return self._current_page

    def makeEmbed(self) -> Embed:
        return self.current_page.makeEmbed()
    
    async def select(self, number: int) -> Page:        
        return await self.current_page.select(number)
    
    async def buttons(self, emoji) -> Page:
        return await self.current_page.buttons(emoji)
        

class LeaguePage(Page):

    no_teams = 'No registered teams.'
    no_games = 'No registered games.'
    active_emoji = '✅'
    inactive_emoji = '❌'

    def __init__(self, user: User, league: LeagueDto, page_message: Message) -> NoReturn:
        super().__init__(user, page_message, \
                [], \
                set(), \
                set())
        
        self.league = league
        self.current_games = [team.current_game for team in league.teams if not team.current_game is None and team.current_game.league is league]

    @property
    def number_of_teams(self) -> int:
        return len(self.league.teams)
    
    @property
    def number_of_games(self) -> int:
        return len(self.current_games)

    def makeEmbed(self) -> Embed:

        embed = Embed(title=self.league.name, color=self.league.color, \
            description=f'{self.number_of_games} current games.\n\
                          {len([team for team in self.league.teams if team.active])} active teams.\n \
                          {len([team for team in self.league.teams if not team.active])} inactive teams.')
        
        
        self.addTeamsField(embed)
        self.addGamesField(embed)
        
        embed.set_footer(text=f'Choose a team by number or go into the games list.\n{LeaguePage.active_emoji} - Active Teams; {LeaguePage.inactive_emoji} - Inactive Teams;')

        return embed

    def addTeamsField(self, embed: embed) -> NoReturn:
        teams_field = '```\n'
        
        for i, team in enumerate(self.league.teams):
            active_status = LeaguePage.active_emoji if team.active else LeaguePage.inactive_emoji
            teams_field += f'{active_status} {i+1:-<10}{team.name:->37}\n'
        
        if teams_field == '```\n':
            teams_field += f'{LeaguePage.no_teams}\n```'
        else:    
            teams_field += '```'

        embed.add_field(name='Registered Teams', value=teams_field, inline=False)
    
    def addGamesField(self, embed: Embed) -> NoReturn:
        games_field = '```\n'
        
        for i, game in enumerate(self.current_games):
            games_field += f'{i+self.number_of_teams+1:-<10}{game.name:->40}\n'
        
        if games_field == '```\n':
            games_field += f'{LeaguePage.no_games}\n```'
        else:
            games_field += '```'

        embed.add_field(name='Current Games', value=games_field, inline=False)

    async def buttons(self, emoji) -> Page:

        return self

    async def select(self, number: int) -> Page:
    
        if 0 < number <= self.number_of_teams:
            new_page = TeamPage(self.user, self.league.teams[number-1], self.page_message)
            await new_page.initPage()
            return new_page
        elif self.number_of_teams < number <= self.number_of_games + self.number_of_teams:
            new_page = GamePage(self.user, self.current_games[number-self.number_of_teams-1], self.page_message)
            await new_page.initPage()
            return new_page
        
        return self


class TeamPage(Page):

    no_leagues = 'No registered leagues.'
    game_emoji = '⚽'
    
    def __init__(self, user: User, team: TeamDto, page_message: Message) -> NoReturn:
        emojis = [TeamPage.game_emoji] if not team.current_game is None else []
        super().__init__(user, page_message, \
                    emojis, \
                    set(), \
                    {ids_letter, keywords_letter, considered_letter})
        self.team = team


    def makeEmbed(self) -> Embed:

        embed = Embed(title=self.team.name, \
                      description=('Active' if self.team.active else 'Inactive'), \
                    )

        self.addLeaguesField(embed)
        self.addCurrentGameField(embed)
        
        addFollowableFields(embed, self.team, self.toggles_on)

        return embed
    
    def addLeaguesField(self, embed: Embed) -> NoReturn:
        leagues_field = '```\n'
        
        for i, league in enumerate(self.team.leagues):
            leagues_field += f'{i+1:-<10}{league.name:->35}\n'
        
        if leagues_field == '```\n':
            leagues_field += f'{TeamPage.no_leagues}\n```'
        else:
            leagues_field += '```'
        
        embed.add_field(name='Registered Leagues', value=leagues_field, inline=False)
        
    def addCurrentGameField(self, embed: Embed) -> NoReturn:
        game = '`No current game.`'

        if self.team.current_game is not None:
            game = '```\n'
            game += f'Name:{self.team.current_game.name:>40}\n'
            game += f'Hours Left:{self.team.current_game.hoursLeft():>34.1f}\n'
            game += '```'
        
        embed.add_field(name='Current Game', value=game, inline=False)


    async def buttons(self, emoji) -> Page:
        if emoji == TeamPage.game_emoji and not self.team.current_game is None:
            new_page = GamePage(self.user, self.team.current_game, self.page_message)
            await new_page.initPage()
            return new_page

        return self

    async def select(self, number: int) -> Page:
        if 0 < number <= len(self.team.leagues):
            new_page = LeaguePage(self.user, self.team.leagues[number-1], self.page_message)
            await new_page.initPage()
            return new_page
        
        return self

class GamePage(Page):

    team_emoji = '🎽'
    league_emoji = '🏆'
    odds_emoji = '💸'

    def __init__(self, user: User, game: GameDto, page_message: Message) -> NoReturn:

        emojis = [GamePage.team_emoji, GamePage.league_emoji, GamePage.odds_emoji]

        toggle_chars = {ids_letter, keywords_letter, considered_letter}

        super().__init__(user, page_message, emojis, set(), toggle_chars)

        self.game = game
    
    @property 
    def game_has_no_odds(self) -> bool:
        return not False in [odds_list == [] for odds_list in self.game.odds.values()]


    def makeEmbed(self) -> Embed:

        embed = Embed(title=self.game.name, \
                              description=str_dates(self.game.date), \
                              color=self.game.league.color)

        
        
        self.addProfileField(embed)
        self.addCurrentOddsField(embed)

        addFollowableFields(embed, self.game, self.toggles_on)

        return embed
    
    def addProfileField(self, embed: Embed) -> NoReturn:
        profile = '```\n'
        profile += f'Team{self.game.team.name:->40}\n'
        profile += f'League{self.game.league.name:->38}\n'
        profile += f'Hours Left{self.game.hoursLeft():->34.1f}\n'
        profile += '```'
        
        embed.add_field(name='Profile', value=profile, inline=False)
    
    def addCurrentOddsField(self, embed: Embed) -> NoReturn:
        if self.game_has_no_odds:
            current_odds = '```\nThis game has no odds.\n```'
        else:
            current_odds = createOddsTable(\
                {site: ('----' if odds_list==[] else [str(odds_list[-1].value)]) for site, odds_list in self.game.odds.items()}, \
                [f'{self.game.hoursLeft():05.1f}'], \
                [site for site in Sites])

        embed.add_field(name='Current Odds', value=current_odds, inline=False)
    
    async def buttons(self, emoji: str) -> Page:

        new_page = None

        if emoji == GamePage.team_emoji:
            new_page = TeamPage(self.user, self.game.team, self.page_message)

        elif emoji == GamePage.league_emoji:
            new_page = LeaguePage(self.user, self.game.league, self.page_message)

        elif emoji == GamePage.odds_emoji:
            new_page = OddsHistoryPage(self.user, self.game, self.page_message)

        if new_page is None:
            return self

        else:
            await new_page.initPage()
            return new_page

    async def select(self, number: int) -> Page:
        return self
    

class OddsHistoryPage(SubPagedPage):

    page_size = 10

    sites_emojis = {Sites.Bwin :   'bwin',
                    Sites.Betano:  'betano',
                    Sites.Betclic: 'betclic',
                    Sites.Solverde:'solverde',
                    Sites.Moosh:   'moosh',
                    Sites.Betway:  'betway'}

    time = 'time left'
    delta = timedelta(hours=1) # timedelta(minutes=6) # use timedelta(seconds=bot.DrawfitBot.update_cycle) for the bots update cycle

    def __init__(self, user: User, game: GameDto, page_message: Message) -> NoReturn:
        
        def oddDate(odd: Optional[OddDto]) -> datetime:
            if odd is None:
                tz = timezone(TIME_ZONE)
                return tz.localize(datetime(year=MAXYEAR, month=1, day=1))
            return odd.date

        emojis = [SubPagedPage.previous_emoji, SubPagedPage.next_emoji]

        toggle_chars = set(OddsHistoryPage.sites_emojis.values())
        
        self.game = game

        self.columns = {site: [] for site in Sites}
        self.columns[OddsHistoryPage.time] = []
        
        # auxiliary structures
        odds_aux = {site: [odd for odd in self.game.odds[site]] for site in Sites}
        terminal = {site: [] for site in Sites}

        while odds_aux != terminal:
            
            # Put newest non-processed odd in odds_buffer
            odds_buffer = {site: (None if odds_aux[site] == [] else odds_aux[site][0]) for site in Sites}
            
            # Choose earliest odd and select other odds that are in the acceptable time frame
            min_odd = min(odds_buffer.values(), key=oddDate)
            odds_buffer = {site: odd for site, odd in odds_buffer.items() if min_odd.date - OddsHistoryPage.delta < oddDate(odd) < min_odd.date + OddsHistoryPage.delta}

            # Generate line of each column
            self.columns[OddsHistoryPage.time].append(f'{min_odd.hours_left:05.1f}')
            for site in Sites:
                self.columns[site].append('----' if not site in odds_buffer else f'{odds_aux[site].pop(0).value:0<4.2f}')

        super().__init__(user, page_message, emojis, set(), toggle_chars, OddsHistoryPage.page_size, len(self.columns[OddsHistoryPage.time]))
        self.toggles_on = self.toggles_on.union(OddsHistoryPage.sites_emojis.values())
        
    
    def makeEmbed(self) -> Embed:

        embed = Embed( title=self.game.name, \
                       description=str_dates(self.game.date), \
                       color=self.game.league.color)

        self.addOddsHistoryField(embed)

        return embed


    def addOddsHistoryField(self, embed: Embed) -> NoReturn:
        odds_history = createOddsTable(\
            {key: value[self.first_page_item:self.last_page_item] for key, value in self.columns.items() if key in self.shownSites}, \
            self.columns[OddsHistoryPage.time][self.first_page_item:self.last_page_item], \
            self.shownSites)

        embed.add_field(name=f'Odds History ({self.page_number}/{self.total_pages})', value=odds_history, inline=False)
        
    
    async def buttons(self, emoji: str) -> Page:

        if emoji == back_emoji:
            new_page = GamePage(self.user, self.domain, self.league, self.game, self.page_message, self.team)
            await new_page.initPage()
            return new_page
        elif emoji == OddsHistoryPage.previous_emoji:
            self.page_number = self.page_number - 1 if self.page_number > 1 else self.total_pages
            self.change = True
        elif emoji == OddsHistoryPage.next_emoji:
            self.page_number = self.page_number + 1 if self.page_number*OddsHistoryPage.page_size <= self.number_of_items else 1
            self.change = True

        return self


    async def select(self, number: int) -> Page:
        return self

    @property
    def shownSites(self) -> List[Sites]:
        return [site for site in Sites if OddsHistoryPage.sites_emojis[site] in self.toggles_on]

class PermissionsPage(Page):
    
    def __init__(self, user: User, page_message: Message, permissions: Dict[Permissions, List[User]]) -> NoReturn:
        super().__init__(user, page_message, \
                [], \
                set(), \
                set())
        
        self.permissions = permissions
    
    
    @abstractmethod
    def makeEmbed(self) -> Embed:
        
        embed = Embed(title='Permissions', description=f'Current bot permissions.')
        
        for perm in Permissions:
            value = ''
            for user in self.permissions[perm]:
                value += f'- {str(user)}\n'
            embed.add_field(name=perm.value, value=value, inline=False)
        
        return embed
        
    
    @abstractmethod
    async def buttons(self, emoji: str) -> Page:
        return self

    async def select(self, number: int) -> Page:
        return self