from enum import Enum
from typing import Generator

valid_sites = []

class Sites(Enum):

    Bwin = 'Bwin'
    Betano = 'Betano'
    Betclic = 'Betclic'
    Solverde = 'Solverde'
    Moosh = 'Moosh'
    Betway = 'Betway'
   
    def small(self) -> str:
        if self == Sites.Bwin:
            return 'BWIN'
        elif self == Sites.Betano:
            return 'BTAN'
        elif self == Sites.Betclic:
            return 'BCLC'
        elif self == Sites.Solverde:
            return 'SOLV'
        elif self == Sites.Moosh:
            return 'MOSH'
        elif self == Sites.Betway:
            return 'BWAY'
    
    def __iter__(self) -> Generator[Site]:
        return (site for site in Sites if site in valid_sites)
        