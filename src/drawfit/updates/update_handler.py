from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, NoReturn, List, Dict, Optional
from requests_html import AsyncHTMLSession

if TYPE_CHECKING:
    from drawfit.domain.notifications import Notification
    from drawfit.domain.domain_store import DomainStore

import drawfit.domain.domain_store as ds

from drawfit.updates.sites.site import Site
from drawfit.updates.sites.bwin import Bwin
from drawfit.updates.sites.betano import Betano
from drawfit.updates.sites.solverde import Solverde
from drawfit.updates.sites.moosh import Moosh
from drawfit.updates.sites.betway import Betway
from drawfit.updates.sites.betclic import Betclic

from drawfit.utils import Sites

class UpdateHandler:

    requests_interval = 1

    def __init__(self, store: DomainStore):
        self.store: DomainStore = store
        self.sites: Dict[Sites, Optional[Site]] = {site: None for site in Sites}
        self.sites[Sites.Bwin] = Bwin()
        self.sites[Sites.Betano] = Betano()
        self.sites[Sites.Solverde] = Solverde()
        self.sites[Sites.Moosh] = Moosh()
        self.sites[Sites.Betway] = Betway()
        self.sites[Sites.Betclic] = Betclic()

    async def update(self) -> List[Notification]:

        codes_by_league = self.store.getAllLeagueCodes()
        session = AsyncHTMLSession()
        results = {}

        # Schedule all requests tasks
        for league, league_codes in codes_by_league.items():

            results[league] = {site: None for site in Sites}
            tasks = {site: None for site in Sites}

            for site in Sites:

                tasks[site] = asyncio.create_task(self.sites[site].getOddsLeague(session, league_codes[site]))

            for site in Sites:

                results[league][site] = await tasks[site]

            await asyncio.sleep(UpdateHandler.requests_interval)
                

        return self.store.updateLeaguesOdds(results)
        

        





