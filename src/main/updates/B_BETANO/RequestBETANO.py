import urllib as u
import requests as r
from datetime import datetime 
from time import localtime, strftime
import json

LEAGUE_ID = '1635'


def buildUrl(leagueID='10210'):
    query = {}
    query['req'] = 'la,s,tn,stnf,c,mb'

    return "https://www.betano.pt/api/sport/futebol/ligas/" + leagueID + "r/?" + u.parse.urlencode(query)


def getOddsLeague(leaguesInfo):
    oddsList = []

    for league in leaguesInfo["data"]["blocks"]:
        for event in league["events"]:
            for market in event["markets"]:
                if market["name"] == "Resultado Final":
                    for bet in market["selections"]:
                        if bet["name"] == "X":
                            oddsList += [(event["name"],bet["price"],betanoEpochConverter(event["startTime"]))]
                            break
                    break
    return oddsList


def betanoEpochConverter(epochTime):
    return datetime.fromtimestamp(epochTime/1000)  


def BETANO_Odds(leagueID=LEAGUE_ID):
    # Creates the request url
    betano_url = buildUrl(leagueID)

    # Makes request to api
    request = r.get(betano_url, headers={"User-Agent": "Mozilla/5.0"})

    # Turn json into data
    info = json.loads(request.text)

    return getOddsLeague(info)