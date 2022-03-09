import asyncio
import websockets as ws
import json
from datetime import datetime


LEAGUE_NAME="Itália - Série B"

def build_url():

    return "wss://sbapi.sbtech.com/mooshpt/sportscontent/sportsbook/v1/Websocket?jwt=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJTZXNzaW9uSVAiOiI4MS44NC4xNzAuMjI2IiwiU2l0ZUlkIjoxNTEsIlZlcnNpb24iOiIyIiwiU2Vzc2lvbklkIjoiZmU5MDljMGItMmUxNy00NzIwLThkZjMtNzc1ZTk3NDZlY2U5IiwibmJmIjoxNjQ2ODQzNDcwLCJleHAiOjE2NDc0NDgzMDAsImlhdCI6MTY0Njg0MzUwMCwiaXNzIjoiQXN5bW1ldHJpY1Rva2VuTWFuYWdlciJ9.US7xvlWQYKftgPLndXwe1-HP6XfZMC9z4lXVNyBa1J-hF9n2CxH1WASTbrCEzNLrqgvGN1k7wibbtl9R8LwvKpMVcnK_yntMwxgY50poN4fR1bs2gNpb9H0unnpqavhe9wjg6GAtsOrdgQ0Qzwpn0N31nEMmknTllgzhqEPsn96O3a5psUDNsBilRhDiaQUPhG8oV42QMSeEibZBtKVqxFP67WRWmRCoWsZA-SMqRZKkvDP4nn7vPYpotsIdVSFd_dZLqInVQtW-mh6NE1Xj8hPFLzBX6SSZ8LOfkE4wsxb37i-de02P4Le9noBtVVzaLRWIFUX7cNfZ9XX4Nvvvpw&locale=pt-pt"


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
    res["method"] = "GetEventsByLeagueId"
    res["meta"] = {"blockId": "eventsWrapper-Center_LeagueViewResponsiveBlock_20002"}
    res["id"] = "7204af80-f77c-4c9a-8fb6-637983a4377a"

    res["params"]["eventTypes"] += ["Fixture", "AggregateFixture"]
    res["params"]["ids"] += [leagueID]
    res["params"]["regionIds"] += [ptID]
    res["params"]["pagination"]["top"] = 100
    res["params"]["pagination"]["skip"] = 0
    res["params"]["marketTypeRequests"] += [{"sportIds": [sportID], "marketTypeIds":["1_0"], "statement": "Include"}]



    return json.dumps(res)


def getSportID(info):
    info = json.loads(info)

    for sport in info["result"]["sports"]:
        if sport["name"] == "Futebol":
            return sport["id"]

def getLeaguePTID(info, leagueName="Itália - Série B"):
    info = json.loads(info)
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
    odds = []
    info = json.loads(info)
    events = info["result"]["events"]
    markets = info["result"]["markets"]

    for i in range(len(events)):
        
        if gameHasPassed(events[i]["startEventDate"]):
            continue

        for bet in markets[i]["selections"]:
            if bet["name"] == "Empate":
                odd = bet["displayOdds"]["decimal"]
        odds += [(events[i]["eventName"], odd, events[i]["startEventDate"])]
    
    return odds



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


async def main_comm(leagueName="Itália - Série B"):

    async with ws.connect(build_url()) as websocket:

        await websocket.send(prepSportsRequest())
        sportID = getSportID(await websocket.recv())

        await websocket.send(prepLeaguesRequest(sportID))
        leagueID, ptID = getLeaguePTID(await websocket.recv(), leagueName)

        await websocket.send(prepEventsRequest(sportID, leagueID, ptID))
        odds = getLeagueOdds(await websocket.recv())

    return odds

print(prepEventsRequest())

result = asyncio.run(main_comm(LEAGUE_NAME))

for odd in result:
    print(odd)