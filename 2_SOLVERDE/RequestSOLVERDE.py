import asyncio
import websockets as ws
import json
from datetime import datetime


# Information to define a league
COUNTRY_CODE='it'
LEAGUE_ID='19328'


# Types of STOMP Messages to send

CONNECT = 0
SUB_REQRES = 1
SUB_ERR = 2


def create_stomp_msg(comd="", headers={}, content=""):

    result = "[\"" + comd + "\\n"

    for header in headers:
        result += str(header) + ":" + str(headers[header]) + "\\n"
    
    result += "\\n" + content + "\\u0000\"]"

    return result

def parse_stomp_msg(msg):


    if len(msg) < 10:
        return {}

    result = ""

    for i in range(4, len(msg)):

        # Next char is start of content
        if (msg[i-4:i] == "\\n\\n"):
            result += msg[i:len(msg)-8]
            break
    
    return json.loads(result.replace('\\', ''))


def msg_dict():

    result = {}
    # Connection message
    result[CONNECT]= create_stomp_msg("CONNECT", {"protocol-version":"1.5", "accept-version":"1.1,1.0", "heart-beat":"10000,10000"})

    # Subscribe request-response api message
    result[SUB_REQRES] = create_stomp_msg("SUBSCRIBE", {"id":"/user/request-response", "destination":"/user/request-response"})

    # Subscribe error api message
    result[SUB_ERR] =  create_stomp_msg("SUBSCRIBE", {"id":"/user/error", "destination":"/user/error"})

    return result


def league_query(ID=19328, country_code='it'):

    id_destination = "/api/eventgroups/soccer-" + country_code + "-sb_type_" + str(ID) + "-all-match-events-grouped-by-type"
    return create_stomp_msg("SUBSCRIBE", {"id":id_destination, "destination":id_destination, "locale":"pt"})

def game_query(ID=4914891889):

    id_destination = "/api/events/" + str(ID)
    return create_stomp_msg("SUBSCRIBE", {"id":id_destination, "destination":id_destination, "locale":"pt"})




def market_query(ID=4914893549):

    id_destination = "/api/markets/" + str(ID)
    return create_stomp_msg("SUBSCRIBE", {"id":id_destination, "destination":id_destination, "locale":"pt"})

def extract_odds(market):

    for bet in market['selectionMap']:
        if market['selectionMap'][bet]['shortName'] == 'X':
            return market['selectionMap'][bet]['prices'][0]['decimalLabel']

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


 
async def main_comm(leagueID=19328, cc='it'):

    messages = msg_dict()

    odds = []

    async with ws.connect("wss://apostas.solverde.pt/api/374/0iiv1wey/websocket") as websocket:

        # get "o" to confirm connetion
        await websocket.recv() 

        # Trade CONNECT messages to establish protocol (I think)
        await websocket.send(messages[CONNECT])
        await websocket.recv() 

        # Subscribe to user/error to get error messages and to user/request-response to be updated on data (most responses sent to this destination, i think
        await websocket.send(messages[SUB_REQRES])
        await websocket.send(messages[SUB_ERR])
        answer = await websocket.recv()

        # Subscribe to league api and obtain event codes
        await websocket.send(league_query(leagueID, cc))
        events = parse_stomp_msg(await websocket.recv())

        # Extract odds of all games in league
        for event in events["groups"][0]["events"]:
            if gameHasPassed(event['startTime']):
                continue
            await websocket.send(game_query(event['id']))
            game = parse_stomp_msg(await websocket.recv())
            

            await websocket.send(market_query(game['marketTypesToIds']['1'][0]))
            market = parse_stomp_msg(await websocket.recv())
                    
            odds += [(game['name'], extract_odds(market), event['startTime'])]

    return odds




result = asyncio.run(main_comm(LEAGUE_ID, COUNTRY_CODE))


for odd in result:
    print(odd)