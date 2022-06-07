import urllib as u

from datetime import datetime
from typing import Dict, List, NoReturn
from requests_html import AsyncHTMLSession
from requests.exceptions import JSONDecodeError

from drawfit.updates.sites.site import Site
from drawfit.updates.exceptions import SiteError
from drawfit.updates.utils import convertDate
from drawfit.utils import Sites, OddSample, BetclicCode


class Betclic(Site):

    url = "https://cds-api.bwin.pt/bettingoffer/fixtures?"

    def __init__(self) -> NoReturn:
        super().__init__([' - '])
    
    async def getOddsLeague(self, session: AsyncHTMLSession, league_code: BetclicCode) -> List[OddSample]:
        """
        Returns the odds of a given league.
        Arguments:
            session - the async session through which the request is made
            leagueId - a dictionary with the following structure {"regionId" : id, "competitionId" : id}
        Throws:
            SiteError - when an error during parsing ocurred
        """
        if self.active and league_code is not None:

            try:

                # Creates the request url
                betclic_url = self.buildUrl(league_id=league_code.id)

                # Makes request to api
                request = await session.get(betclic_url, headers={"User-Agent": "Mozilla/5.0"})

                # Gets the odds from the info
                return self.parseResponse(request.json())

            except Exception:
                return None
                #raise SiteError(Sites.Betclic.name)

        else:
            return None
    

    def parseResponse(self, leaguesInfo) -> List[OddSample]:
        oddsList = []
        for event in leaguesInfo["unifiedEvents"]:
            
            for market in event["markets"]:
                if market["name"] == "Resultado (Tempo Regulamentar)":
                    for bet in market["selections"]:
                        if bet["name"] == "Empate":
                            oddsList.append(OddSample(self.getTeams(event["name"]), float(bet["odds"]), convertDate(event["date"]), datetime.now()))
        
        return oddsList


    def buildUrl(self, league_id="30"):
        query = {}
        query["application"] = "1024"
        query["countrycode"] = "pt"
        query["fetchMultipleDefaultMarkets"] = "true"
        query["forceCompetitionInfo"] = "true"
        query["language"] = "pt"

        return "https://offer.cdn.begmedia.com/api/pub/v2/competitions/" + league_id + "?" + u.parse.urlencode(query)
