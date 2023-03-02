from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, NoReturn, List, Dict, Optional
from requests_html import AsyncHTMLSession

if TYPE_CHECKING:
    from drawfit.domain.notifications import Notification
    from drawfit.domain.domain_store import DomainStore

import drawfit.domain.domain_store as ds

from drawfit.updates.sites import Site, Bwin, Betano, Solverde, Moosh, Betway, Betclic

from drawfit.utils import Sites, create_new_logger

class UpdateHandler:

    requests_interval = 0.1
    logger_name = 'updates'

    def __init__(self, store: DomainStore):
        self.store: DomainStore = store
        self.sites: Dict[Sites, Optional[Site]] = {site: None for site in Sites}
        self.logger = create_new_logger(UpdateHandler.logger_name)
        
        self.sites[Sites.Bwin] = Bwin()
        self.sites[Sites.Betano] = Betano()
        self.sites[Sites.Betclic] = Betclic()
        self.sites[Sites.Solverde] = Solverde()
        self.sites[Sites.Moosh] = Moosh()
        # Betway and Moosh deactivated for now
        self.sites[Sites.Betway] = Betway()
        self.sites[Sites.Betway].active = False
        
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
                try:
                    results[league][site] = await tasks[site]
                except:
                    self.logger.debug(f'Exception occurred when trying to parse odds from {site.name}', exc_info=True)

            await asyncio.sleep(UpdateHandler.requests_interval)

        return self.store.updateLeaguesOdds(results)
        

        





