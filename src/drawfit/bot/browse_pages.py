from __future__ import annotations

from abc import abstractmethod
from datetime import datetime, timedelta, MAXYEAR
from typing import NoReturn, List, Optional, Set


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

def addFollowableFields(embed: Embed, followable: FollowableDto, toggle_on: Set[str]) -> NoReturn:
    if ids_emoji in toggle_on:
            ids = '```\n'
            for site, id in followable.ids.items():
                print(site)
                print(id)
                ids += f'{site.name:-<10}{id if id is not None else no_id:->20}\n'
            ids += '```'
            embed.add_field(name=f'{ids_emoji} - Ids', value=ids, inline=False)

    if keywords_emoji in toggle_on:
        keywords = '`No Keywords`'

        if followable.keywords != []:
            keywords = '```\n'
            for number, keyword in enumerate(followable.keywords):
                keywords += f'{number+1:02}{keyword:->20}\n'
            keywords += '```'

        embed.add_field(name=f'{keywords_emoji} - Keywords', value=keywords, inline=False)

    if considered_emoji in toggle_on:
        considered = '```\n'
        for site, considered_ids in followable.considered.items():
            considered += f'{site.name}\n'

            if considered_ids == []:
                considered += f'{no_considered_ids:->20}\n'
            else:
                for number, considered_id in enumerate(considered_ids):
                    considered += f'  {number+1:02}{considered_id:->18}\n'
            
        considered += '```'
        embed.add_field(name=f'{considered_emoji} - Considered Ids', value=considered, inline=False)

class Page:

    def __init__(self, user: User, domain: DomainDto, page_message: Message, all_emojis: List[str], toggle_emojis: Set[str]) -> NoReturn:
        self.user = user
        self.domain = domain
        self.page_message = page_message

        self.emojis = all_emojis
        self.all_toggles = toggle_emojis

        self.toggles_on = set()
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
        super().__init__(user, domain, page_message, [DomainPage.codes_emoji], {DomainPage.codes_emoji})

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
                        {LeaguePage.act_teams_emoji, LeaguePage.inact_teams_emoji, LeaguePage.games_emoji})
        
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
                    [back_emoji, ids_emoji, keywords_emoji, considered_emoji, TeamPage.game_emoji], \
                    {ids_emoji, keywords_emoji, considered_emoji})
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
    sites_emojis = {Sites.Bwin :   '🟡',
                    Sites.Betano:  '🟠',
                    Sites.Betclic: '🔴',
                    Sites.Solverde:'🟢',
                    Sites.Moosh:   '🟣',
                    Sites.Betway:  '⚪'}
    no_team = 'Team not found'
    time = 'time left'
    delta = timedelta(seconds=bot.DrawfitBot.update_cycle)# timedelta(seconds=360) # use timedelta(seconds=bot.DrawfitBot.update_cycle) for the bots update cycle

    def __init__(self, user: User, domain: DomainDto, league: LeagueDto, game: GameDto, page_message: Message, team: Optional[TeamDto]=None) -> NoReturn:
        
        def oddDate(odd: Optional[OddDto]) -> datetime:
            if odd is None:
                return datetime(year=MAXYEAR, month=1, day=1)
            return odd.date

        emojis = [back_emoji, ids_emoji, keywords_emoji, considered_emoji, GamePage.odds_emoji]
        emojis.extend([GamePage.sites_emojis[site] for site in Sites])

        toggle_emojis = {ids_emoji, keywords_emoji, considered_emoji, GamePage.odds_emoji}
        toggle_emojis = toggle_emojis.union(GamePage.sites_emojis.values())

        super().__init__(user, domain, page_message, emojis, toggle_emojis)

        self.league = league
        self.team = team
        self.game = game

        self.toggles_on = self.toggles_on.union(GamePage.sites_emojis.values())

        self.columns = {site: [] for site in Sites}
        self.columns[GamePage.time] = []
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

                odds_buffer = {site: odd for site, odd in odds_buffer.items() if min_odd.date - GamePage.delta < oddDate(odd) < min_odd.date + GamePage.delta}

                self.columns[GamePage.time].append(f'{min_odd.hours_left:02.1f}')
                

                for site in Sites:
                    if site in odds_buffer:
                        current_indexes[site] += 1
                        self.columns[site].append(f'{odds_buffer[site].value:1.2f}')
                    else:
                        self.columns[site].append(f'----')


    def makeEmbed(self) -> Embed:

        embed = Embed(title=self.game.name, \
                              description=(self.game.date), \
                              color=self.league.color)

        teams = '```\n'
        teams += f'Team1 {GamePage.no_team if self.game.team1 is None else self.game.team1:>40}\n'
        teams += f'Team2 {GamePage.no_team if self.game.team2 is None else self.game.team2:>40}\n'
        teams += '```'
        embed.add_field(name='Teams', value=teams, inline=False)

        addFollowableFields(embed, self.game, self.toggles_on)

        if self.show_odds:
            odds = '```\n'

            column_labels = ['time']
            for site in self.shownSites:
                column_labels.append(f'{site.small()}')
            
            line = '|'.join(column_labels)
            odds += f'{line}\n'
            odds += len(line) * '=' + '\n'


            for i, time in enumerate(self.columns[GamePage.time]):
                line = [time]

                for site in self.shownSites:
                    line.append(f'{self.columns[site][i]:>4}')
                
                line = '|'.join(line)
                odds += f'{line}\n'


            odds += '\nCurrent odds:\n'

            if self.columns[GamePage.time] == []:
                last_line = ['This game has no odds.']
            
            else:
                last_line = [self.columns[GamePage.time][-1]]

                for _, odd in self.game.odds.items():

                    if odd == []:
                        last_line.append('----')
                    else:
                        last_line.append(f'{odd[-1].value:1.2f}')
                

            odds += '|'.join(last_line) + '\n'

            odds += '```'
            embed.add_field(name='Odds History', value=odds, inline=False)


        footer = ''
        for site in Sites:
            footer += f'{GamePage.sites_emojis[site]} - {site.name}\n'
        embed.set_footer(text=footer)
        return embed
    
    async def buttons(self, emoji: str) -> Page:

        if emoji == back_emoji and self.team is not None:
            new_page = TeamPage(self.user, self.domain, self.league, self.team, self.page_message)
            await new_page.initPage()
            return new_page
        elif emoji == back_emoji:
            new_page = LeaguePage(self.user, self.domain, self.league, self.page_message)
            await new_page.initPage()
            return new_page

        return self

    async def select(self, number: int) -> Page:
        return self
    
    @property
    def show_odds(self) -> bool:
        return GamePage.odds_emoji in self.toggles_on

    @property
    def shownSites(self) -> List[Sites]:
        return [site for site in Sites if GamePage.sites_emojis[site] in self.toggles_on]

