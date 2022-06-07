import urllib as u

from datetime import datetime
from typing import Dict, List, NoReturn
from requests_html import AsyncHTMLSession
from requests.exceptions import JSONDecodeError

from drawfit.updates.sites.site import Site
from drawfit.updates.exceptions import SiteError
from drawfit.updates.utils import convertMilisecondsEpoch
from drawfit.utils import Sites, OddSample, BetanoCode


class Betano(Site):

    url = "https://www.betano.pt/api/sport/futebol/ligas/"

    def __init__(self) -> NoReturn:
        super().__init__([' - '])
    
    async def getOddsLeague(self, session: AsyncHTMLSession, league_code: BetanoCode) -> List[OddSample]:
        if self.active and league_code is not None:

            try:

                # Creates the request url
                betano_url = self.buildUrl(league_code.id)

                # Makes request to api
                request = await session.get(betano_url, headers={"User-Agent": "Mozilla/5.0"})

                # Gets the odds from the info
                return self.parseResponse(request.json())

            except Exception:
                return None
                #raise SiteError(Sites.Betano.name)

        else:
            return None

    def buildUrl(self, leagueID: str = '10210') -> str:
        query = {}
        query['req'] = 'la,s,tn,stnf,c,mb'

        return Betano.url + leagueID + "r/?" + u.parse.urlencode(query)


    def parseResponse(self, leaguesInfo) -> List[OddSample]:
        oddsList = []

        if leaguesInfo["data"] is None:
            return oddsList

        for league in leaguesInfo["data"]["blocks"]:
            for event in league["events"]:
                for market in event["markets"]:
                    if market["name"] == "Resultado Final":
                        for bet in market["selections"]:
                            if bet["name"] == "X":
                                oddsList.append(OddSample(self.getTeams(event["name"]), float(bet["price"]), convertMilisecondsEpoch(event["startTime"]), datetime.now()))
                                break
                        break
        return oddsList
