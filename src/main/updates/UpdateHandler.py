<<<<<<< HEAD
import asyncio


class UpdateHandler:
    def __init__(self):
        pass

    async def run(self):
        while(True):
            print("Reached UpdateHandler")
=======
import asyncio

from domain.DomainStore import DomainStore


class UpdateHandler:
    def __init__(self, store: DomainStore):
        self.store = store

    async def run(self):
        while(True):
            print("Reached UpdateHandler")
>>>>>>> TestCommandsLibrary
            await asyncio.sleep(3600)