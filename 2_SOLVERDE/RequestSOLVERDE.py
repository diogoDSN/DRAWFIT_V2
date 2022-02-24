import asyncio
import websockets as ws
import stomp.utils as stomp

async def main_comm():
    async with ws.connect("wss://apostas.solverde.pt/api/374/0iiv1wey/websocket") as websocket:
        
        # get "o" to confirm connetion
        answer = await websocket.recv() 
        print("Recv: " + answer)

        # Trade CONNECT messages to establish protocol (I think)
        await websocket.send("[\"CONNECT\\nprotocol-version:1.5\\naccept-version:1.1,1.0\\nheart-beat:10000,10000\\n\\n\\u0000\"]")
        print("Sent: CONNECT request")
        answer = await websocket.recv() 
        print("Recv: " + answer)

        # Subscribe to user/error to get error messages and to user/request-response to be updated on data (most responses sent to this destination, i think)
        await websocket.send("[\"SUBSCRIBE\\nid:/user/request-response\\ndestination:/user/request-response\\n\\n\\u0000\"]")
        print("Sent: SUBSCRIBE user/request-response request")
        await websocket.send("[\"SUBSCRIBE\\nid:/user/error\\ndestination:/user/error\\n\\n\\u0000\"]")
        print("Sent: SUBSCRIBE user/error request")
        answer = await websocket.recv()
        print("Recv: " + answer)

        # Subscribe to league api and obtain event codes
        await websocket.send("[\"SUBSCRIBE\\nid:/api/eventgroups/soccer-it-sb_type_19328-all-match-events-grouped-by-type\\ndestination:/api/eventgroups/soccer-it-sb_type_19328-all-match-events-grouped-by-type\\nlocale:pt\\n\\n\\u0000\"]")
        print("Sent: SUBSCRIBE eventgroups/soccer-it-sb_type_19328-all-match-events-grouped-by-type request")
        answer = await websocket.recv()
        print("Recv: " + answer)


    return


asyncio.run(main_comm())