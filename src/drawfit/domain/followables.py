from datetime import datetime
from typing import NoReturn, List, Tuple

from drawfit.domain.odd import Odd

from drawfit.utils import Sites, OddSample

class Followable:

    # constructor

    def __init__(self, keywords: List[str] = []) -> NoReturn:
        self._keywords: List[str] = keywords
        self._considered: Dict[Sites, Optional[List[Tuple[str]]]] = {site: [] for site in Sites}
        self._ids: Dict[Sites, Optional[Tuple[str]]] = {site: None for site in Sites}
        self._complete: bool = False

    # properties

    @property
    def keywords(self) -> List[str]:
        return self._keywords
    
    def addKeywords(self, new_keywords: List[str]) -> NoReturn:
        self._keywords.extend(new_keywords)
    
    def removeKeywords(self, to_remove: List[str]) -> NoReturn:
        self._keywords = list(filter(lambda x: x not in to_remove, self._keywords))
    
    @property
    def considered(self) -> List[List[str]]:
        return self._considered
    
    def addConsidered(self, site: Sites, considered: Tuple[str]) -> NoReturn:
        self._considered[site].append(considered)
    
    def removeConsidered(self, site: Sites, considered: Tuple[str]):
        self._considered[site].remove(considered)
    
    @property
    def ids(self) -> List[Tuple[str]]:
        return self._ids
    
    def setId(self, site: Sites, id: Tuple[str]) -> NoReturn:
        self._ids[site] = id

        if None not in self.ids:
            self._complete = True
    
    @property
    def complete(self) -> bool:
        return self._complete

    # followable logic
    
    def isId(self, site: Sites, id: Tuple[str]) -> bool:
        return self.ids[site] == id
    
    def couldBeId(self, site: Sites, id: Tuple[str]) -> bool:

        if self.ids[site] is not None or id in self.considered[site]:
            return False
        
        for keyword in self.keywords:
            for name in id:
                if name in keyword or keyword in name:
                    return True
        
        return False


class Game(Followable):

    def __init__(self, name: str, date: datetime = None, keywords: List[Tuple[str]] = []):
        
        super().__init__(keywords)

        # Set universal undefined values
        self._name: str = name
        self._date: datetime = date
        self._odds = {site: [] for site in Sites}
        

    @property
    def name(self) -> str:
        return self._name

    @property
    def date(self) -> datetime:
        return self._date
    
    @date.setter
    def date(self, date: datetime) -> NoReturn:
        if self.date == None:
            self._date = date
    
    @property
    def odds(self) -> List[List[Odd]]:
        return self._odds

    def __eq__(self, o):
        if o.__class__ == self.__class__:
            return self.name == o.name and self.date == o.date
        return False       

    def addOdd(self, sample: OddSample, site: Sites) -> bool:

        if self.odds[site] == [] or self.odds[site][-1].value != sample.odd:
            self.odds[site].append(Odd(sample.odd, sample.sample_time))
            return True
        
        return False
        

class Team(Followable):

    def __init__(self, name: str):
        super().__init__()
        self._name = name
        self._active: bool = True
    
    @property
    def name(self) -> str:
        return self._name
    
    def __eq__(self, o) -> bool:
        if o.__class__ == self.__class__:
            return self.name == o.name
        
        return False