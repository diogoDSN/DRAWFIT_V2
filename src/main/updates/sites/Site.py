from abc import abstractmethod

from requests_html import AsyncHTMLSession

class Site:

    def __init__(self):
        self.active = True

    @abstractmethod
    async def getOddsLeague(self, session: AsyncHTMLSession, leagueId: str) -> list:
        pass
    
    def deactivate(self):
        self.active = False

