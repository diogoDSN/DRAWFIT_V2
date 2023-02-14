from __future__ import annotations

from datetime import datetime, timedelta
from pytz import timezone
from typing import NoReturn, List, Tuple, Dict, Optional, TYPE_CHECKING

import drawfit.domain.odd as o

if TYPE_CHECKING:
    from drawfit.domain.league import League

from drawfit.utils import Sites, OddSample, now_lisbon

class Followable:

    # constructor

    def __init__(self, keywords: Optional[List[Tuple[str]]] = None) -> NoReturn:
        if keywords == None:
            keywords = []

        self._keywords: List[str] = keywords
        self._considered: Dict[Sites, List[Tuple[str]]] = {site: [] for site in Sites}
        self._ids: Dict[Sites, Optional[Tuple[str]]] = {site: None for site in Sites}

    # properties

    @property
    def keywords(self) -> List[str]:
        return self._keywords
    
    def addKeywords(self, new_keywords: List[str]) -> NoReturn:
        self._keywords.extend(new_keywords)
    
    def removeKeywords(self, to_remove: List[str]) -> NoReturn:
        self._keywords = list(filter(lambda x: x not in to_remove, self._keywords))
    
    @property
    def considered(self) -> Dict[Sites, List[Tuple[str]]]:
        return self._considered
    
    def addConsidered(self, site: Sites, considered: Tuple[str]) -> NoReturn:
        self._considered[site].append(considered)
    
    def removeConsidered(self, site: Sites, considered: Tuple[str]):
        self._considered[site].remove(considered)
    
    @property
    def ids(self) -> Dict[Sites, Optional[Tuple[str]]]:
        return self._ids
    
    def setId(self, site: Sites, id: Tuple[str]) -> NoReturn:
        self._ids[site] = id

    # followable logic
    
    def isId(self, site: Sites, id: Tuple[str]) -> bool:
        return self._ids[site] == id
    
    def couldBeId(self, site: Sites, id: Tuple[str]) -> bool:

        if self._ids[site] is not None or id in self.considered[site]:
            return False
        
        for keyword in self.keywords:
            for name in id:
                if name in keyword or keyword in name:
                    return True
        
        return False
    
    def resetIds(self) -> NoReturn:
        self._ids = {site: None for site in Sites}
        



class Game(Followable):

    def __init__(self, name: str, date: datetime, team: Team, league: l.League):

        super().__init__([])

        # Set universal undefined values
        self._name: str = name
        self._date: datetime = date
        self._odds = {site: [] for site in Sites}
        self._team = team
        self._league = league
        

    @property
    def name(self) -> str:
        return self._name

    @property
    def date(self) -> datetime:
        return self._date
    
    @date.setter
    def date(self, date: datetime) -> NoReturn:
        self._date = date
    
    @property
    def odds(self) -> Dict[Sites, List[o.Odd]]:
        return self._odds

    @property
    def team(self) -> Team:
        return self._team
    
    @property
    def league(self) -> l.League:
        return self._league

    def hoursLeft(self, time: datetime = None) -> float:

        if self.date is None:
            return 0

        if time is None:
            time = now_lisbon()

        delta = self.date - time
        return delta.total_seconds() / 3600

    def __eq__(self, o):
        if isinstance(o, Game):
            return self.name == o.name and self.date == o.date
        return False
    
    def canUpdateDate(self, sample: OddSample) -> bool:
        return self.date < sample.start_time
    
    def canAddOdd(self, odd_value: float, odd_datetime: datetime, site: Sites) -> bool:
        return self.odds[site] == [] or self.odds[site][-1].value != odd_value
            

    def addOdd(self, odd_value: float, odd_datetime: datetime, site: Sites) -> bool:

        if self.canAddOdd(odd_value, odd_datetime, site):
            self._odds[site].append(o.Odd(odd_value, odd_datetime, self))

            current_odds = {each_site: (0 if self.odds[each_site] == [] else self.odds[each_site][-1].value) for each_site in Sites}

            previous_odds = dict(current_odds)
            previous_odds[site] = 0 if len(self.odds[site]) == 1 else self.odds[site][-2].value

            # Notification is sent when: 
            #  #1 A new odd becomes the current highest 
            #  #2 An odd rises to match the highest
            if all(self.odds[site][-1].value >= value for value in current_odds.values()) or \
              (all(previous_odds[site] >= value for value in previous_odds.values()) and any(current_odds[site] < value for value in current_odds.values())):
                return True
        
        return False
        

class Team(Followable):

    delta = timedelta(hours=30)

    def __init__(self, name: str):
        super().__init__([name])
        self._name = name
        self._active: bool = True
        self._current_game = None
        self._leagues = {}
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def active(self) -> bool:
        return self._active
    
    @active.setter
    def active(self, active: bool) -> NoReturn:
        self._active = active
    
    @property
    def current_game(self) -> Optional[Game]:
        return self._current_game
    
    @current_game.setter
    def current_game(self, game: Optional[Game]) -> NoReturn:
        self._current_game = game
    
    @property
    def leagues(self) -> Dict[League]:
        return self._leagues
    
    def addLeague(self, league: League) -> NoReturn:
        self._leagues[league.name] = league
    
    def hasGame(self) -> bool:
        return not self.current_game is None
    
    def isCurrentGame(self, date: datetime, league: l.League) -> bool:
        return self.hasGame() and self.current_game.date - Team.delta  < date < self.current_game.date + Team.delta and league is self.current_game.league
    
    def __eq__(self, o) -> bool:
        if isinstance(o, Team):
            return self.name == o.name
        
        return False
    
    def __repr__(self) -> str:
        return f'Name: {self.name}; Game: {self.current_game};\nKeywords: {self.keywords}; Considered: {self.considered}; Ids: {self._ids};'