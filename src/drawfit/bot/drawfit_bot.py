from __future__ import annotations

import asyncio
import pickle

from typing import List, Dict, Tuple, TYPE_CHECKING, NoReturn

import discord
from discord.ext import commands

import drawfit.domain.domain_store as store
import drawfit.updates.update_handler as updates

from drawfit.bot.permissions import Permissions
from drawfit.utils import Sites

if TYPE_CHECKING:
    import drawfit.domain.notifications as notf


class DrawfitBot(commands.Bot):

    store_path = "/tmp/test_data.pickle"
    greeting = '**Hello there!** - Obi-Wan Kenobi'
    update_cycle = 30
    command_timeout = 7
    command_channels = {'Vascolândia': ['private-nogueira']}
    update_channels = {'Vascolândia' : ['private-nogueira-2']}
    permissions = {Permissions.NOGUEIRA: ['Pistache#2173'], \
                            Permissions.MODERATOR: [], \
                            Permissions.NORMAL: ['File_Read_Bot#9655']}
    
    def __init__(self):

        intents = discord.Intents.default()
        intents.members = True
        super().__init__(command_prefix='.', intents=intents)

        try:
            with open(DrawfitBot.store_path, 'rb') as f:
                self.store = pickle.load(f)
        except Exception:
            self.store = store.DomainStore()
        
        self.pending_queries: List[asyncio.Task] = []
        self.routines: List[asyncio.Task] = []

        self.configureCommands()
    
    def setInitialPermissions(self):

        perms = {}

        for permission, perms_list in DrawfitBot.permissions.items():
            
            current_perms = []

            for user in self.get_all_members():
                if str(user) in perms_list:
                    current_perms.append(user)
            
            perms[permission] = current_perms
        
        return perms
    
    def configureCommands(self):
        import drawfit.bot.commands as cmd

        for name, attribute in cmd.__dict__.items():
            try:
                if callable(attribute):
                    self.add_command(attribute)
            except TypeError:
                pass

    async def greet(self):

        all_channels = self.getChannels(DrawfitBot.command_channels)
        all_channels.extend(self.getChannels(DrawfitBot.update_channels))

        for channel in all_channels:
            await channel.send(DrawfitBot.greeting)    

    async def on_ready(self):

        self.perms: Dict[Permissions, List[discord.User]] = self.setInitialPermissions()

        # prepare visitor
        from drawfit.bot.notify import Notify
        self.notification_visitor = Notify(self)
        self.notify_tasks = []
    
        self.routines.append(asyncio.create_task(self.store.removeRoutine()))

        await self.greet()

        self.routines.append(asyncio.create_task(self.handlerRoutine()))


    async def handlerRoutine(self):

        handler = updates.UpdateHandler(self.store)

        while(True):

            print('Update Started')

            notifications = await handler.update()

            print(f'Update ended. With {len(notifications)} notifications')

            for notification in notifications:
                self.notify(notification)

            print('All notification tasks created')

            await asyncio.sleep(DrawfitBot.update_cycle)
    
    async def on_command_error(self, ctx, error):
        if error.__class__ == commands.BadArgument:
            await ctx.send(error)
        elif error.__class__ == commands.CommandNotFound:
            pass
        else:
            raise error
    

    def notify(self, notification: notf.Notification) -> NoReturn:
        self.notify_tasks.append(asyncio.create_task(notification.accept(self.notification_visitor)))

    def teamIdAccepted(self, team_name: str, team_id: Tuple[str], site: Sites, league_name: str):
        self.store.setTeamId(team_name, team_id, site, league_name)
        
    def gameIdAccepted(self, game_name: str, game_id: Tuple[str], site: Sites, league_name: str):
        self.store.setGameId(game_name, game_id, site, league_name)
    
    def endTask(self, task: asyncio.Task):
        self.notify_tasks.remove(task)

    def getUsersWithPermission(self, perm: Permissions) -> List[discord.User]:

        users = []

        if perm == Permissions.NORMAL:
            users += self.perms[perm]
            perm = Permissions.MODERATOR

        if perm == Permissions.MODERATOR:
            users += self.perms[perm]
            perm = Permissions.NOGUEIRA

        if perm == Permissions.NOGUEIRA:
            users += self.perms[perm]
        
        return users
    
    def getChannels(self, channels_names: Dict[str, List[str]]):

        channels = []

        for guild_name in channels_names:
            guild = discord.utils.get(self.guilds, name=guild_name)

            if guild is None:
                continue

            for channel_name in channels_names[guild_name]:
                channel = discord.utils.get(guild.text_channels, name=channel_name)

                if channel is None:
                    continue

                channels.append(channel)

        return channels  
    
    def save(self) -> bool:
        try:
            with open(DrawfitBot.store_path, 'wb') as f:
                pickle.dump(self.store, f)
            
            return True
        except Exception:
            pass
        
        return False
