import domain.classes.Team as team
import domain.classes.Game as game


from typing import List, NoReturn
from domain.classes.Sites import Sites
from updates.sites.utils import OddSample


class League:

    def __init__(self, name: str):
        
        self.name: str = name
        self.leagueCodes: List[str] = []
        self.currentGames: List[game.Game] = []
        self.gamesQueue: List[str] = []
        self.followedTeams: List[team.Team] = []
        self._active: bool = True

        for _ in Sites:
            self.leagueCodes.append(None)

    @property
    def active(self) -> bool:
        return self._active

    @property
    def currentGames(self) -> list[game.Game]:
        return self.currentGames

    @property
    def followedTeams(self) -> list[team.Team]:
        return self.followedTeams

    def updateLeaguesOdds(self, samples_by_site: List[List[OddSample]]) -> NoReturn:
        for site in Sites:

            if samples_by_site[site.value] is None:
                continue

            for sample in samples_by_site[site.value]:
                pass
