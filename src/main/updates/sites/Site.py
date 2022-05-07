from abc import abstractmethod

from requests_html import AsyncHTMLSession

class Site:

    @abstractmethod
    async def getOddsLeague(self, session: AsyncHtmlSession, leagueId: str) -> list:
        pass


