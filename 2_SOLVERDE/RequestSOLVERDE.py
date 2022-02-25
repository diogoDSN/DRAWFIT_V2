import asyncio
import websockets as ws
import json


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


def league_game_query(ID=19328):

    id_destination = "/api/eventgroups/soccer-it-sb_type_" + ID + "-all-match-events-grouped-by-type"
    return create_stomp_msg("SUBSCRIBE", {"id":id_destination, "destination":id_destination, "locale":"pt"})

def extract_odds(info):


async def main_comm(leagueID=19328):

    messages = msg_dict()


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
        await websocket.send(league_game_query(leagueID))
        events = parse_stomp_msg(await websocket.recv())

        # note: this structures also contains start times
        odds = []
        for event in events["groups"][0]["events"]:
            await websocket.send(league_game_query(event['id']))
            answer = parse_stomp_msg(await websocket.recv())

            odds = extract_odds(answer) 

    return

asyncio.run(main_comm())