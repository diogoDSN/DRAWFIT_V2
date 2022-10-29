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
   
    def small(self) -> Optional[str]:
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
    
    @classmethod
    def SiteFromName(site_name: str) -> Optional[Sites]:
        return next((site for site in Sites if site.value == site_name), None)
    
    def __iter__(self) -> Generator[Site]:
        return (site for site in Sites if site in valid_sites)
        