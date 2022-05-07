import asyncio

from pandas import DataFrame as df

from domain.DomainStore import DomainStore


class UpdateHandler:
    def __init__(self, store: DomainStore):
        self.store = store
        self.last_odds = {}
        
        for league in store.getLeagues():


    async def run(self):
        while(True):
            print("Reached UpdateHandler")
            await asyncio.sleep(3600)