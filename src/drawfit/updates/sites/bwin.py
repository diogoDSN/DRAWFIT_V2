import urllib as u

from typing import Dict, List, NoReturn
from requests_html import AsyncHTMLSession

from drawfit.updates.sites.site import Site
from drawfit.updates.utils import convertDate
from drawfit.utils import Sites, OddSample, BwinCode, now_lisbon


class Bwin(Site):

    url = "https://cds-api.bwin.pt/bettingoffer/fixtures?"

    def __init__(self) -> NoReturn:
        super().__init__([' - '])
    
    async def getOddsLeague(self, session: AsyncHTMLSession, league_code: BwinCode) -> List[OddSample]:
        """
        Returns the odds of a given league.
        Arguments:
            session - the async session through which the request is made
            leagueId - a dictionary with the following structure {"regionId" : id, "competitionId" : id}
        """
        if self.active and league_code is not None:

            # Creates the request url
            bwin_url = self.buildUrl(region_id=league_code.region_id, competition_id=league_code.competition_id)

            # Makes request to api
            request = await session.get(bwin_url, headers={"User-Agent": "Mozilla/5.0"})

            # Gets the odds from the info
            return self.parseResponse(request.json())

        else:
            return None
    

    def parseResponse(self, league_info) -> List[OddSample]:
        """
        Extracts odds from a league's odd information.
        league_info - a json with the league's odd information
        Throws ValueError if there was a failure reading data from the json
        """
        oddsList = []
        now = now_lisbon()
        # Fixtures are information packages on specific games
        for game in league_info['fixtures']:
            # optionMarkets are the available markets to bet on for this game
            for market in game['optionMarkets']:
                if market['name']['value'] == 'Resultado do jogo':
                    # Options contains the multiles bet options in this market
                    for bet in market['options']:
                        if bet['name']['value'] == 'X':
                            # Append tupple (game, odd) to the list off obtained odds
                            oddsList.append(OddSample(self.getTeams(game['name']['value']), float(bet['price']['odds']), convertDate(game['startDate']), now))
        
        return oddsList


    def buildUrl(self, region_id : str ='20', competition_id: str ='102848') -> str:
        query = {}
        query['x-bwin-accessid'] = 'YmQwNTFkNDAtNzM3Yi00YWIyLThkNDYtYWFmNGY2N2Y1OWIx'
        query['lang'] = 'pt'
        query['country'] = 'PT'
        query['userCountry'] = 'PT'
        query['fixtureTypes'] = 'Standard'
        query['state'] = 'Latest'
        query['offerMapping'] = 'Filtered'
        query['offerCategories'] = 'Gridable'
        query['fixtureCategories'] = 'Gridable,NonGridable,Other'
        query['sportIds'] = '4'
        query['regionIds'] = region_id
        query['competitionIds'] = competition_id
        query['skip'] = '0'
        query['take'] = '50'
        query['sortBy'] = 'tags'
    
        return Bwin.url + u.parse.urlencode(query)
