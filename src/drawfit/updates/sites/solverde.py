import urllib as u
import json
import websockets as ws
from datetime import datetime
from typing import List, NoReturn
from requests_html import AsyncHTMLSession


from drawfit.updates.sites.site import Site
from drawfit.updates.exceptions import SiteError
from drawfit.updates.utils import convertDate
from drawfit.utils import Sites, OddSample, SolverdeCode


def create_stomp_msg(comd="", headers={}, content=""):

    result = "[\"" + comd + "\\n"

    for header in headers:
        result += str(header) + ":" + str(headers[header]) + "\\n"
    
    result += "\\n" + content + "\\u0000\"]"

    return result


class Solverde(Site):

    # Information to define a league
    timeout = 3.0


    # Types of STOMP Messages to send

    CONNECT = create_stomp_msg("CONNECT", {"protocol-version":"1.5", "accept-version":"1.1,1.0", "heart-beat":"10000,10000"})
    SUB_REQRES = create_stomp_msg("SUBSCRIBE", {"id":"/user/request-response", "destination":"/user/request-response"})
    SUB_ERR = create_stomp_msg("SUBSCRIBE", {"id":"/user/error", "destination":"/user/error"})

    def __init__(self) -> NoReturn:
        super().__init__(' - ')
    
    async def getOddsLeague(self, _: AsyncHTMLSession,  league_code: SolverdeCode) -> List[OddSample]:
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

                odds = []

                async with ws.connect("wss://apostas.solverde.pt/api/374/0iiv1wey/websocket", open_timeout=Solverde.timeout) as websocket:

                    # get "o" to confirm connetion
                    await websocket.recv() 

                    # Trade CONNECT messages to establish protocol (I think)
                    await websocket.send(Solverde.CONNECT)
                    await websocket.recv() 

                    # Subscribe to user/error to get error messages and to user/request-response to be updated on data (most responses sent to this destination, i think
                    await websocket.send(Solverde.SUB_REQRES)
                    await websocket.send(Solverde.SUB_ERR)
                    answer = await websocket.recv()

                    # Subscribe to league api and obtain event codes
                    await websocket.send(self.league_query(league_code.league_id, league_code.country_code))
                    events = self.parse_stomp_msg(await websocket.recv())

                    # Extract odds of all games in league
                    for event in events["groups"][0]["events"]:
                        await websocket.send(self.game_query(event['id']))
                        game = self.parse_stomp_msg(await websocket.recv())
                        

                        await websocket.send(self.market_query(game['marketTypesToIds']['1'][0]))
                        market = self.parse_stomp_msg(await websocket.recv())
                                
                        odds.append(OddSample(self.getTeams(game['name']), float(self.extract_odds(market)), convertDate(event['startTime']), datetime.now()))

                return odds

            except json.JSONDecodeError:
                raise SiteError(Sites.Solverde.name)

        else:
            return None

    
    def league_query(self, id: str = '19328', country_code: str = 'it'):

        id_destination = "/api/eventgroups/soccer-" + country_code + "-sb_type_" + id + "-all-match-events-grouped-by-type"
        return create_stomp_msg("SUBSCRIBE", {"id":id_destination, "destination":id_destination, "locale":"pt"})

    def game_query(self, ID=4914891889):

        id_destination = "/api/events/" + str(ID)
        return create_stomp_msg("SUBSCRIBE", {"id":id_destination, "destination":id_destination, "locale":"pt"})
    
    def market_query(self, ID=4914893549):

        id_destination = "/api/markets/" + str(ID)
        return create_stomp_msg("SUBSCRIBE", {"id":id_destination, "destination":id_destination, "locale":"pt"})

    def parse_stomp_msg(self, msg):


        if len(msg) < 10:
            return {}

        result = ""

        for i in range(4, len(msg)):

            # Next char is start of content
            if (msg[i-4:i] == "\\n\\n"):
                result += msg[i:len(msg)-8]
                break
        
        return json.loads(result.replace('\\', ''))
    
    def extract_odds(self, market):

        for bet in market['selectionMap']:
            if market['selectionMap'][bet]['shortName'] == 'X':
                return market['selectionMap'][bet]['prices'][0]['decimalLabel']
