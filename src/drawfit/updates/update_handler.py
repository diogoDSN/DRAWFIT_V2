import asyncio
from typing import NoReturn, List
from requests_html import AsyncHTMLSession

from drawfit.domain.notifications import Notification
from drawfit.domain.domain_store import DomainStore

from drawfit.updates.sites.bwin import Bwin
from drawfit.updates.sites.site import Site

from drawfit.utils import Sites

class UpdateHandler:
    
    def __init__(self, store: DomainStore):
        self.store: DomainStore = store
        self.sites: List[Site] = [None for _ in Sites]
        self.sites[Sites.Bwin.value] = Bwin()


    async def update(self) -> List[Notification]:

        codes_by_league = self.store.getAllLeagueCodes()
        print("Codes -", codes_by_league)
        session = AsyncHTMLSession()
        requests = {}
        results = {}

        # Schedule all requests tasks
        for league, league_codes in codes_by_league.items():

            requests[league] = [None for _ in Sites]

            for site in Sites:
                requests[league][site.value] = asyncio.create_task(self.sites[site.value].getOddsLeague(session, league_codes[site.value]))

        print("Requests -", requests)

        # Await every created task for results
        for league, league_requests in requests.items():

            results[league] = [None for _ in Sites]

            for site, site_request in enumerate(league_requests):
                results[league][site] = await site_request
        
        print("Results -", results)
            
        return self.store.updateLeaguesOdds(results)
        

        





