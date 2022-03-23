import urllib as u
import requests as r
from datetime import datetime 
from time import localtime, strftime
import json

LEAGUE_ID = "30"


def buildUrl(leagueID="30"):
    query = {}
    query["application"] = "1024"
    query["countrycode"] = "pt"
    query["fetchMultipleDefaultMarkets"] = "true"
    query["forceCompetitionInfo"] = "true"
    query["language"] = "pt"

    return "https://offer.cdn.begmedia.com/api/pub/v2/competitions/" + leagueID + "?" + u.parse.urlencode(query)


def getOddsLeague(leaguesInfo):
    oddsList = []
    for event in leaguesInfo["unifiedEvents"]:
        if gameHasPassed(event["date"]):
            continue
        
        for market in event["markets"]:
            if market["name"] == "Resultado (Tempo Regulamentar)":
                for bet in market["selections"]:
                    if bet["name"] == "Empate":
                        oddsList += [(event["name"], bet["odds"], event["date"])]
    
    return oddsList




# info" date format: "2022-02-20T17:00:00Z"
def gameHasPassed(datetimeInfo):
    # Create time vector
    now = datetime.now()
    curr_times = (now.year, now.month, now.day, now.hour, now.minute, now.second)

    aux_str = ""
    i = 0
    for c in datetimeInfo:
        if c not in ("-", ":", "T", "Z"):
            if aux_str == "" and c == "0":
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

def BETCLIC_Odds(leagueID=LEAGUE_ID):

    # Creates the request url
    betclic_url = buildUrl(leagueID)

    # Makes request to api
    request = r.get(betclic_url, headers={"User-Agent": "Mozilla/5.0"})

    # Turn json into data
    info = json.loads(request.text)


    return getOddsLeague(info)


