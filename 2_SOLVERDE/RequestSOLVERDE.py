import asyncio
import websockets


async def getLeagueOdds():
    async with websockets.connect() as ws:
        answer = await ws.recv()
        print(answer)


# Extracts info from api
asyncio.run(getLeagueOdds())