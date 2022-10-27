from abc import abstractmethod
from typing import NoReturn, Tuple, List
from requests_html import AsyncHTMLSession

from drawfit.utils import OddSample, LeagueCode

class Site:

    def __init__(self, site_vs_strings: List[str]) -> NoReturn:
        self.active = True
        self.site_vs_strings = site_vs_strings

    @abstractmethod
    async def getOddsLeague(self, session: AsyncHTMLSession, league_id: LeagueCode) -> List[OddSample]:
        pass

    def deactivate(self) -> bool:
        self.active = False


    def getTeams(self, game_name: str) -> Tuple[str]:
        for string in self.site_vs_strings:
            if string in game_name:
                return tuple(game_name.split(string))
