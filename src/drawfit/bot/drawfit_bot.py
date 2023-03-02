from __future__ import annotations

import asyncio
import logging
import json
from os import environ
from typing import List, Dict, Tuple, TYPE_CHECKING, NoReturn, Optional

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
        
        self.perms: Dict[Permissions, List[discord.User]] = {perm: [] for perm in Permissions}

        self.configureCommands()
    
    def setInitialPermissions(self):

        try:
            with open('./permissions/perms.json', 'r') as perm_file:
                permissions_string = json.load(perm_file)
                permissions = {perm: permissions_string[perm.value] for perm in Permissions}
                
                if permissions[Permissions.OWNER] == []:
                    raise FileNotFoundError()
                
                self.logger.debug(f'Booting from file permissions')
        except FileNotFoundError or KeyError:
            permissions = {perm: [] for perm in Permissions}
            permissions[Permissions.OWNER] = [environ['OWNER_USERNAME']]
            self.logger.debug(f'Booting from default permissions')
        except:
            self.logger.critical(f'An error occurred when trying to read the permissions file.', exc_info=True)
            return

        for permission, perms_list in permissions.items():
            
            for username in perms_list:
                self.setPermission(permission, username)
        
        if self.perms[Permissions.OWNER] == []:
            self.logger.critical(f'No owner set in permissions!')
    
    def setPermission(self, permission: Optional[Permissions], username: str) -> NoReturn:
        
        if (perm:=self.getPermission(username)) is not None:
            self.perms[perm] = [user for user in self.perms[perm] if str(user) != username]
        
        
        if permission is not None:
            for member in self.get_all_members():
            
                if str(member) == username:
                    self.perms[permission].append(member)
                    break
        
        serializable_perms = {perm.value: [str(user) for user in self.perms[perm]] for perm in Permissions}
        
        json_perms = json.JSONEncoder().encode(serializable_perms)
        
        with open('./permissions/perms.json', 'w') as perm_file:
            perm_file.write(json_perms)
    
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
        
        self.setInitialPermissions()

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
            try:

                self.logger.debug('Update Started.')

                notifications = await handler.update()

                if len(notifications) != 0:
                    self.logger.debug(f'Creating {len(notifications)} notifications.')

                for notification in notifications:
                    await asyncio.sleep(1)
                    self.notify(notification)

                self.logger.debug('Update Ended.')

                await asyncio.sleep(DrawfitBot.update_cycle)
            
            except:
                self.logger.critical(f'Exception occurred in update cycle:', exc_info=True)
    
    async def on_command_error(self, ctx, error):
        if error.__class__ == commands.BadArgument:
            await ctx.send(error)
        elif error.__class__ == commands.CommandNotFound:
            pass
        else:
            self.logger.error(f'Command error on: [{ctx.message.content}].\n{error}', exc_info=True)
    
    def notify(self, notification: notf.Notification) -> NoReturn:
        self.notify_tasks.append(asyncio.create_task(notification.accept(self.notification_visitor)))

    def teamIdAccepted(self, team_name: str, team_id: Tuple[str], site: Sites, league_name: str):
        self.store.setTeamId(team_name, team_id, site, league_name)
    
    def endTask(self, task: asyncio.Task):
        self.notify_tasks.remove(task)

    def getPermission(self, username: str) -> Optional[Permissions]:
        if username in [str(user) for user in self.perms[Permissions.NORMAL]]:
            return Permissions.NORMAL
        elif username in [str(user) for user in self.perms[Permissions.MODERATOR]]:
            return Permissions.MODERATOR
        elif username in [str(user) for user in self.perms[Permissions.OWNER]]:
            return Permissions.OWNER
        
        return None

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
