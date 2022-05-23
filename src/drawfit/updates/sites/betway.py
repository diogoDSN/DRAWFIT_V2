import urllib as u
import json
import websockets as ws
from datetime import datetime
from typing import List, NoReturn
from requests_html import AsyncHTMLSession


from drawfit.updates.sites.site import Site
from drawfit.updates.exceptions import SiteError
from drawfit.updates.utils import convertDate
from drawfit.utils import Sites, OddSample, BetwayCode


class Betway(Site):

    # Information to define a league
    timeout = 3.0

    # Types of STOMP Messages to send

    def __init__(self) -> NoReturn:
        super().__init__(' vs ')
    
    async def getOddsLeague(self, session: AsyncHTMLSession,  league_code: BetwayCode) -> List[OddSample]:
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

                async with ws.connect(await self.build_url(session), open_timeout=Betway.timeout) as websocket:

                    await websocket.send(self.prepSportsRequest())
                    sportID = self.getSportID(await websocket.recv())

                    await websocket.send(self.prepLeaguesRequest(sportID))
                    leagueID, ptID = self.getLeaguePTID(await websocket.recv(), league_code.name)

                    await websocket.send(self.prepEventsRequest(sportID, leagueID, ptID))
                    odds = self.getLeagueOdds(await websocket.recv())

                return odds

            except Exception:
                return None
                #raise SiteError(Sites.Betway.name)

        else:
            return None
        
    

    async def build_url(self, session: AsyncHTMLSession):

        raw_info = await session.get(url="https://api.play-gaming.com/auth/v2/GetTokenBySiteId/194", headers={"User-Agent": "Mozilla/5.0"})
        WebToken = raw_info.json()["token"]

        return "wss://sbapi.sbtech.com/betwaypt/sportscontent/sportsbook/v1/Websocket?jwt=" + WebToken + "&locale=pt"


        
    def prepSportsRequest(self):
        res = {}
        res["jsonrpc"] = "2.0"
        res["params"] = {"eventState": "Mixed"}
        res["method"] = "GetSports"
        res["meta"] = {"blockId": "sportsContent"}
        res["id"] = "fb02ec02-1480-4f0c-a93d-d9a2d4cef256"
        return json.dumps(res)

    def prepLeaguesRequest(self, sportID="1"):
        res = {}
        res["jsonrpc"] = "2.0"
        res["params"] = {"ids":[], "includeRegions":True}
        res["method"] = "GetLeaguesBySportId"
        res["meta"] = {"blockId": "sportsContent"}
        res["id"] = "a73d9ceb-84b1-49f7-aeeb-1ceb80a20dd8"

        res["params"]["ids"] += [sportID]

        return json.dumps(res)

    def prepEventsRequest(self, sportID="1", leagueID="42884", ptID='180'):
        #TODO might want to to bulk all league requests in this one query
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


    def getSportID(self, info):
        info = json.loads(info)

        for sport in info["result"]["sports"]:
            if sport["name"] == "Futebol":
                return sport["id"]

    def getLeaguePTID(self, info, leagueName="Itália - Série B"):
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
    
    
    def getLeagueOdds(self, info):
        odds = []
        info = json.loads(info)

        events = info["result"]["events"]
        markets = info["result"]["markets"]

        diff = len(events) - len(markets)


        for i, market in enumerate(markets):
            
            for bet in market["selections"]:
                if bet["name"] == "Empate":
                    odd = bet["displayOdds"]["decimal"]

            odds.append(OddSample(self.getTeams(events[i + diff]["eventName"]), float(odd), convertDate(events[i]["startEventDate"]), datetime.now()))
        
        return odds
