import sys
from os.path import dirname, abspath

sys.path.append(dirname(dirname(abspath(__file__))) + '/main')

import asyncio
from typing import Dict
from requests_html import AsyncHTMLSession
from updates.sites.Bwin import Bwin
from updates.sites.Site import Site



async def testSiteInfo(webSite: Site, siteName: str, session: AsyncHTMLSession, leagueId: Dict[str, str]):
    results = await webSite.getOddsLeague(session, leagueId)
    print("---" + siteName + " START---")
    for odd in results:
        print(odd)

    print("---" + siteName + " END---\n")

async def main():

    session = AsyncHTMLSession()

    print("START TESTS:\n")

    await testSiteInfo(Bwin(), "BWIN", session, {"regionId": '20', "competitionId": '102846'})

    print("END TESTS\n")

asyncio.run(main())