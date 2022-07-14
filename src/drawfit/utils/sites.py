from enum import Enum

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
        