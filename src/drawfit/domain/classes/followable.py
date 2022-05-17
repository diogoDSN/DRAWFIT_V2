from typing import NoReturn, List, Tuple

from drawfit.utils import Sites

class Followable:

    # constructor

    def __init__(self, keywords: List[str] = []) -> NoReturn:
        self._keywords: List[str] = keywords
        self._considered: List[List[Tuple[str]]] = [[] for _ in Sites]
        self._ids: List[Tuple[str]] = [None for _ in Sites]
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
        self._considered[site.value].append(considered)
    
    def removeConsidered(self, site: Sites, considered: Tuple[str]):
        self._considered[site.value].remove(considered)
    
    @property
    def ids(self) -> List[Tuple[str]]:
        return self._ids
    
    def setId(self, site: Sites, id: Tuple[str]) -> NoReturn:
        self._ids[site.value] = id

        if None not in self.ids:
            self._complete = True
    
    @property
    def complete(self) -> bool:
        return self._complete

    # followable logic
    
    def isId(self, site: Sites, id: Tuple[str]) -> bool:
        return self.ids[site.value] == id
    
    def couldBeId(self, site: Sites, id: Tuple[str]) -> bool:

        if self.ids[site.value] is not None or id in self.considered[site.value]:
            return False
        
        for keyword in self.keywords:
            for name in id:
                if name in keyword or keyword in name:
                    return True
        
        return False
