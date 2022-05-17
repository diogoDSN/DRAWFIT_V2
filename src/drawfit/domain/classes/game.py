from datetime import datetime
from typing import NoReturn, List, Tuple

import drawfit.domain as domain
from drawfit.utils import Sites, OddSample


class Game(domain.Followable):

    def __init__(self, name: str, date: datetime = None, keywords: List[Tuple[str]] = []):
        
        super().__init__(keywords)

        # Set universal undefined values
        self._name: str = name
        self._date: datetime = date
        self._odds = [[] for _ in Sites]
        

    @property
    def name(self) -> str:
        return self._name.join

    @property
    def date(self) -> datetime:
        return self._date
    
    @date.setter
    def date(self, date: datetime) -> NoReturn:
        if self.date == None:
            self._date = date
    
    @property
    def odds(self) -> List[List[domain.Odd]]:
        return self._odds

    def __eq__(self, o):
        if o.__class__ == self.__class__:
            return self.name == o.name and self.date == o.date
        return False       

    def addOdd(self, sample: OddSample, site: Sites) -> bool:

        if self.odds[site.value] == [] or self.odds[site.value][-1].value != sample.odd:
            self.odds[site.value].append(domain.Odd(sample.odd, sample.sample_time))
            return True
        
        return False
        
        