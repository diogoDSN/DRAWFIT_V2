import urllib as u
import requests as r
from datetime import datetime 
from time import localtime, strftime
import json

LEAGUE_ID = '10210'


def buildUrl(leagueID='10210'):
    query = {}
    query['req'] = 'la,s,tn,stnf,c,mb'

    return "https://www.betano.pt/api/sport/futebol/ligas/" + leagueID + "r/?" + u.parse.urlencode(query)


def getOddsLeague(leaguesInfo):
    oddsList = []

    for league in leaguesInfo["data"]["blocks"]:
        for event in league["events"]:
            if gameHasPassed(betanoEpochConverter(event["startTime"])):
                continue
            for market in event["markets"]:
                if market["name"] == "Resultado Final":
                    for bet in market["selections"]:
                        if bet["name"] == "X":
                            oddsList += [(event["name"],bet["price"],betanoEpochConverter(event["startTime"]))]
                            break
                    break
    return oddsList


def betanoEpochConverter(epochTime):
    return strftime('%Y-%m-%dT%H:%M:%SZ', localtime(epochTime))


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
betano_url = buildUrl(LEAGUE_ID)

# Makes request to api
request = r.get(betano_url, headers={"User-Agent": "Mozilla/5.0"})

# Turn json into data
info = json.loads(request.text)


odds = getOddsLeague(info)

# Print the odds colected in an orderly manner
for odd in odds:
    print(odd)