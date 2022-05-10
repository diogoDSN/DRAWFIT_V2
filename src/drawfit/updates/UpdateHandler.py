import asyncio
from typing import NoReturn, List
from domain.classes.Sites import Sites
from updates.sites.Bwin import Bwin
from updates.sites.Site import Site
from requests_html import AsyncHTMLSession

from domain.DomainStore import DomainStore


class UpdateHandler:
    
    def __init__(self, store: DomainStore):
        self.store: DomainStore = store
        self.sites: List[Site] = [None for _ in Sites]
        self.sites[Sites.BWIN.value] = Bwin()


    async def update(self) -> List:

        codes_by_league = self.store.getAllLeagueCodes()
        session = AsyncHTMLSession()
        results = {}

        # Schedule all requests tasks
        for league, league_codes in codes_by_league.items():

            results[league] = [None for _ in Sites]

            for site in Sites:
                results[league][site.value] = asyncio.create_task(self.sites[site.value].getOddsLeague(session, league_codes[site.value]))

        # Await every created task for results
        for league_results in results:
            for site, result in enumerate(league_results):
                league_results[site] = await result
            
        return self.store.updateLeaguesOdds(results)
        

        




