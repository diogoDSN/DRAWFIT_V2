from typing import List, NoReturn


import drawfit.domain as domain
from drawfit.utils import Sites


class Team(domain.Followable):

    def __init__(self, name: str):
        super().__init__()
        self._active: bool = True
    
    @property
    def name(self) -> str:
        return self._name
    
    def __eq__(self, o) -> bool:
        if o.__class__ == self.__class__:
            return self.name == o.name
        
        return False

