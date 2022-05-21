import asyncio

from typing import List, Dict, Tuple

import discord
from discord.ext import commands

import drawfit.domain.domain_store as store
import drawfit.updates.update_handler as updates

from drawfit.bot.permissions import Permissions
from drawfit.utils import Sites


class DrawfitBot(commands.Bot):

    greeting = 'Hello there! - Obi-Wan Kenobi'
    command_timeout = 7
    command_channels = {'Vascolândia': ['private-nogueira']}
    update_channels = {'Vascolândia' : ['private-nogueira-2']}
    permissions = {Permissions.NOGUEIRA: ['Pistache#2173'], \
                            Permissions.MODERATOR: [], \
                            Permissions.NORMAL: ['Periquito#0366', 'Peter Pie#3256']}
    
    def __init__(self):

        intents = discord.Intents.default()
        intents.members = True
        super().__init__(command_prefix='.', intents=intents)

        self.store = store.DomainStore()
        
        self.pending_queries: List[asyncio.Task] = []

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
    
        
        await self.greet()

        self.handler_routine = asyncio.create_task(self.handlerRoutine())

    async def on_command_error(self, ctx, error):
        if error.__class__ == commands.BadArgument:
            await ctx.send(error)
        elif error.__class__ == commands.CommandNotFound:
            pass
        else:
            raise error

    async def handlerRoutine(self):

        handler = updates.UpdateHandler(self.store)

        print("Reached Update Handler")
        while(True):

            print("Update Started!")

            notifications = await handler.update()

            print(f"Update Ended! With {len(notifications)} notifications pending!")

            for notification in notifications:
                self.notify_tasks.append(asyncio.create_task(notification.accept(self.notification_visitor)))
            
            print("All notification tasks created! Waiting next update!")

            await asyncio.sleep(30)
    
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
