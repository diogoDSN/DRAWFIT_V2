from abc import abstractmethod
from typing import NoReturn, Tuple, List
from requests_html import AsyncHTMLSession

from drawfit.utils import OddSample, LeagueCode

class Site:

    def __init__(self, site_vs_string: str) -> NoReturn:
        self.active = True
        self.site_vs_string = site_vs_string

    @abstractmethod
    async def getOddsLeague(self, session: AsyncHTMLSession, league_id: LeagueCode) -> List[OddSample]:
        pass

    def deactivate(self) -> bool:
        self.active = False


    def getTeams(self, game_name: str) -> Tuple[str]:
        return tuple(game_name.split(self.site_vs_string))
