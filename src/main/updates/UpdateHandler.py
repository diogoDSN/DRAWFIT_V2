import asyncio


class UpdateHandler:
    def __init__(self):
        pass

    async def run(self):
        while(True):
            print("Reached UpdateHandler")
            await asyncio.sleep(3600)