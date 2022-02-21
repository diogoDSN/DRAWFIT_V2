import urllib as u
import requests as r
from datetime import datetime 
import json

REGION_ID = '20'
COMPETITION_ID = '102848'


def buildQuery(regionID='20', competitionID='102848'):
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
    
    return u.parse.urlencode(query)


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
                        oddsList.append((game['name']['value'], bet['price']['odds']))
    
    return oddsList


# info' date format: "2022-02-20T17:00:00Z"
def gameHasPassed(datetimeInfo):
    # Create time vector
    now = datetime.now()
    curr_times = (now.year, now.month, now.day, now.hour, now.minute, now.second)

    aux_str = ""
    i = 0
    for c in datetimeInfo:
        if c not in ('-', ':', 'T', 'Z'):
            if aux_str == "" and c == '0':
                continue

            aux_str += c

        else:
            if aux_str == "":
                aux_str = "0"
            game_time = eval(aux_str)

            # Game time is before current time
            if game_time < curr_times[i]:
                return True
            
            # Game time is after current time
            elif game_time > curr_times[i]:
                return False

            # This current and game time component coincide [for example both in the same year]
            i += 1
            aux_str = ""

    return False

def updateDataBase(newOdds):
    # Opens database for updating
    database = open("Bwin_data.json", '+')

    # Reads full database
    oldDataJson = database.read(None)

    # Parses json
    oldData = json.loads(oldDataJson)

    #TODO


# Creates the request url
bwin_url = "https://cds-api.bwin.pt/bettingoffer/fixtures?" + buildQuery(competitionID=COMPETITION_ID, regionID=REGION_ID)

# Makes request to api
request = r.get(bwin_url, headers={"User-Agent": "Mozilla/5.0"})

# Turn json into data
info = json.loads(request.text)

# Gets the odds from the info
odds = getOddsLeague(info)


# Print the odds colected in an orderly manner
for odd in odds:
    print(odd)