import urllib as u

from updates.sites.Site import Site

class Bwin(Site):

    url = "https://cds-api.bwin.pt/bettingoffer/fixtures?"

    def __init__(self):
        self.last_odds = {}
    

    def update_odds

    def BWIN_Odds(competitionID=COMPETITION_ID, regionID=REGION_ID):

        # Creates the request url
        bwin_url =  buildUrl(competitionID=competitionID, regionID=regionID)

        # Makes request to api
        request = r.get(bwin_url, headers={"User-Agent": "Mozilla/5.0"})

        # Turn json into data
        info = json.loads(request.text)

        # Gets the odds from the info
        odds = getOddsLeague(info)

        return odds

    def getOddsLeague(leagueInfo):
        oddsList = []
        # Fixtures are information packages on specific games
        for game in leagueInfo['fixtures']:
            # Test if game has passed [started]
            if gameHasPassed(game['startDate']):
                continue

            # optionMarkets are the available markets to bet on for this game
            for market in game['optionMarkets']:
                if market['name']['value'] == 'Resultado do jogo':
                    # Options contains the multiles bet options in this market
                    for bet in market['options']:
                        if bet['name']['value'] == 'X':
                            # Append tupple (game, odd) to the list off obtained odds
                            oddsList.append((game['name']['value'], bet['price']['odds'], game['startDate']))
        
        return oddsList


    def addQuery(self, regionID='20', competitionID='102848'):
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
        query['regionIds'] = regionID
        query['competitionIds'] = competitionID
        query['skip'] = '0'
        query['take'] = '50'
        query['sortBy'] = 'tags'
    
        return Bwin.url + u.parse.urlencode(query)