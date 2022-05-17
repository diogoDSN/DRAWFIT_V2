import asyncio
from typing import NoReturn, List
from requests_html import AsyncHTMLSession

import drawfit.domain as domain
import drawfit.updates as updates

from drawfit.utils import Sites

class UpdateHandler:
    
    def __init__(self, store: domain.DomainStore):
        self.store: domain.DomainStore = store
        self.sites: List[updates.Site] = [None for _ in Sites]
        self.sites[Sites.BWIN.value] = updates.Bwin()


    async def update(self) -> List[domain.Notification]:

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
        

        





