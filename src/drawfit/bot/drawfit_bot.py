from __future__ import annotations

import asyncio
import logging
from typing import List, Dict, Tuple, TYPE_CHECKING, NoReturn

import discord
from discord.ext import commands

from drawfit.parameters import PERMISSIONS, COMMAND_CHANNELS, UPDATES_CHANNELS, QUERIES_CHANNELS

import drawfit.database.database_store as db_store
import drawfit.domain.domain_store as store
import drawfit.updates.update_handler as updates

from drawfit.bot.permissions import Permissions
from drawfit.utils import Sites, valid_sites, create_new_logger

if TYPE_CHECKING:
    import drawfit.domain.notifications as notf


class DrawfitBot(commands.Bot):

    greeting = '**Hello there!** - Obi-Wan Kenobi'
    logger_name = 'bot'
    update_cycle = 30
    
    def __init__(self):

        intents = discord.Intents.all()
        super().__init__(command_prefix='.', intents=intents)

        global valid_sites
        with db_store.DatabaseStore() as db:
            valid_sites.extend(db.getAllSites())
        
        self.store = store.DomainStore()
        
        self.pending_queries: List[asyncio.Task] = []
        self.routines: List[asyncio.Task] = []
        self.setup = False

        self.logger = create_new_logger(DrawfitBot.logger_name)

        self.configureCommands()
    
    def setInitialPermissions(self):

        perms = {}

        for permission, perms_list in PERMISSIONS.items():
            
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

        all_channels = self.getChannels(COMMAND_CHANNELS)
        all_channels.extend(self.getChannels(UPDATES_CHANNELS))
        all_channels.extend(self.getChannels(QUERIES_CHANNELS))

        for channel in all_channels:
            await channel.send(DrawfitBot.greeting)    

    async def on_ready(self):

        if self.setup:
            return
        
        self.setup = True

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

            self.logger.debug('Update Started.')

            notifications = await handler.update()

            if len(notifications) != 0:
                self.logger.debug(f'Creating {len(notifications)} notifications.')

            for notification in notifications:
                await asyncio.sleep(1)
                self.notify(notification)

            self.logger.debug('Update Ended.')

            await asyncio.sleep(DrawfitBot.update_cycle)
    
    async def on_command_error(self, ctx, error):
        if error.__class__ == commands.BadArgument:
            await ctx.send(error)
        elif error.__class__ == commands.CommandNotFound:
            pass
        else:
            self.logger.error(f'{error} on command error.', exc_info=True)
    
    def notify(self, notification: notf.Notification) -> NoReturn:
        self.notify_tasks.append(asyncio.create_task(notification.accept(self.notification_visitor)))

    def teamIdAccepted(self, team_name: str, team_id: Tuple[str], site: Sites, league_name: str):
        self.store.setTeamId(team_name, team_id, site, league_name)
    
    def endTask(self, task: asyncio.Task):
        self.notify_tasks.remove(task)

    def getUsersWithPermission(self, perm: Permissions) -> List[discord.User]:

        users = []

        if perm == Permissions.NORMAL:
            users += self.perms[perm]
            perm = Permissions.MODERATOR

        if perm == Permissions.MODERATOR:
            users += self.perms[perm]
            perm = Permissions.OWNER

        if perm == Permissions.OWNER:
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
