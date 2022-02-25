import asyncio
import websockets as ws
import json
from datetime import datetime


def build_url():

    return "wss://sbapi.sbtech.com/mooshpt/sportscontent/sportsbook/v1/Websocket?jwt=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJTZXNzaW9uSVAiOiIxNzYuNzguMjYuMTMwIiwiU2l0ZUlkIjoxNTEsIlZlcnNpb24iOiIyIiwiU2Vzc2lvbklkIjoiZTQ1ZTFmNzctNjg0OS00NmVmLTgzYTQtM2IwZDc5NzQ4YzE5IiwibmJmIjoxNjQ1Nzg5MDA3LCJleHAiOjE2NDYzOTM4MzcsImlhdCI6MTY0NTc4OTAzNywiaXNzIjoiQXN5bW1ldHJpY1Rva2VuTWFuYWdlciJ9.LdMjqv34g_F1gCHics_7lk7YL6c_22yYiMc2lmLkaIdIyNsUx8Nd5wDdHGbd9jqipjtxET3pFc1yrdhcTrvyIDwf-EyCMLtk3S_2pVxucNPl4-cUxB-75bJasRMFacyGPw2gJj0eL_OVn2nc5j-rB1HtONCx6GVjIQa-_IXbds1ffIzYmKM0FK_iszouCOganneKjJWLIFkaWta8D8X8D5ox2fgbfbhTAE4mSQktSjhf6Ae0jZr3bfp8r0TymMGXNdaYN7lk71bGsFLsXtYpScVQdUQvd4XqzGZ_L_yBOZ-4qeKbtRi6r35kbVeroQpaaqr4sGwUVkKzTV739Vtt-Q&locale=pt-pt"


def prepSportsRequest():
    res = {}
    res["jsonrpc"] = "2.0"
    res["params"] = {"eventState": "Mixed"}
    res["method"] = "GetSports"
    res["meta"] = {"blockId": "sportsContent"}
    res["id"] = "fb02ec02-1480-4f0c-a93d-d9a2d4cef256"
    return json.dumps(res)

def prepLeaguesRequest(sportID="1"):
    res = {}
    res["jsonrpc"] = "2.0"
    res["params"] = {"ids":[], "includeRegions":True}
    res["method"] = "GetLeaguesBySportId"
    res["meta"] = {"blockId": "sportsContent"}
    res["id"] = "a73d9ceb-84b1-49f7-aeeb-1ceb80a20dd8"

    res["params"]["ids"] += [sportID]

    return json.dumps(res)

#TODO might be worth it to hust request all the needed leagues
def prepEventsRequest(sportID="1", leagueID="42884", ptID=180):
    res={}
    res["jsonrpc"] = "2.0"
    res["params"] = {"eventState": "Mixed", "eventTypes": [], "ids":[], "regionIds":[], "pagination":{}, "marketTypeRequests":[]}
    res["method"] = "GetEventsByLeague"
    res["meta"] = {"blockId": "eventsWrapper-Center_LeagueViewResponsiveBlock_20002"}
    res["id"] = "7204af80-f77c-4c9a-8fb6-637983a4377a"

    res["params"]["eventTypes"] += ["Fixture", "AggregateFixture"]
    res["params"]["ids"] += [leagueID]
    res["params"]["regionIds"] += [ptID]
    res["params"]["pagination"]["top"] = 100
    res["params"]["pagination"]["skip"] = 0
    res["params"]["marketTypeRequests"] += {"sportIds": [sportID], "marketTypeIds":["1_0"], "statement": "Include"}


    return json.dumps(res)


def getSportID(info):
    info = json.decoder(info)

    for sport in info["result"]["sports"]:
        if sport["name"] == "Futebol":
            return sport["id"]

def getLeaguePTID(info, leagueName="Itália - Série B"):
    info = json.decoder(info)
    leagueID = ""
    regionID = ""
    for league in info["result"]["leagues"]:
        if league["name"] == leagueName:
            leagueID = league["id"]
            break
    
    for region in info["result"]["regions"]:
        if region["code"] == "PT":
            regionID = region["id"]
            break
    
    return leagueID, regionID

def getLeagueOdds(info):
    info = json.decoder(info)
    for market in 



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


async def main_comm():

    odds = []

    async with ws.connect(build_url()) as websocket:

        await websocket.send(prepSportsRequest())
        print(await websocket.recv())

    return odds

result = asyncio.run(main_comm())

for odd in result:
    print(odd)