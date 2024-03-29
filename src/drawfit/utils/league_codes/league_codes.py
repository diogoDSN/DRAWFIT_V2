import re
from abc import abstractmethod
from typing import Optional

from drawfit.utils.sites import Sites
from drawfit.utils.league_codes.league_code_error import LeagueCodeError

class LeagueCode:

    def __init__(self, raw_code: str, pattern: str, error_msg: str):
        if not re.search(pattern, raw_code):
            raise LeagueCodeError(error_msg)

    @abstractmethod
    def getSite(self) -> Sites:
        pass



class BwinCode(LeagueCode):

    pattern = '\\A\\d{1,4},\\d{5,7}\\Z'
    error_msg = 'Invalid bwin league code! A bwin league code follows the format:\n `0000,000000`'

    def __init__(self, raw_code: str):
        
        super().__init__(raw_code, BwinCode.pattern, BwinCode.error_msg)
        self.region_id, self.competition_id = raw_code.split(',')

    def getSite(self) -> Sites:
        return Sites.Bwin
    
    def __str__(self) -> str:
        return f'{self.region_id},{self.competition_id}'

class BetanoCode(LeagueCode):

    pattern = '\\A\\d{4,6}\\Z'
    error_msg = 'Invalid betano league code! A betano league code follows the format:\n `00000`'

    def __init__(self, raw_code: str):
        
        super().__init__(raw_code, BetanoCode.pattern, BetanoCode.error_msg)
        self.id = raw_code

    def getSite(self) -> Sites:
        return Sites.Betano

    def __str__(self) -> str:
        return f'{self.id}'

class SolverdeCode(LeagueCode):

    pattern = '\\A[a-zA-Z0-9]{1,6},\\d{4,6}\\Z'
    error_msg = 'Invalid solverde league code! A solverde league code follows the format:\n `aa,00000`'

    def __init__(self, raw_code: str):
        
        super().__init__(raw_code, SolverdeCode.pattern, SolverdeCode.error_msg)
        self.country_code, self.league_id = raw_code.split(',')

    def getSite(self) -> Sites:
        return Sites.Solverde

    def __str__(self) -> str:
        return f'{self.country_code},{self.league_id}'

class MooshCode(LeagueCode):

    pattern = '\\A.*\\Z'
    error_msg = 'Invalid moosh league code! A moosh league code follows the format:\n `Itália - Série B`'

    def __init__(self, raw_code: str):

        super().__init__(raw_code, MooshCode.pattern, MooshCode.error_msg)
        self.name = raw_code

    def getSite(self) -> Sites:
        return Sites.Moosh
    
    def __str__(self) -> str:
        return f'{self.name}'

class BetwayCode(LeagueCode):

    pattern = '\\A.*\\Z'
    error_msg = 'Invalid betway league code! A betway league code follows the format:\n `Itália - Série B`'

    def __init__(self, raw_code: str):
        
        super().__init__(raw_code, BetwayCode.pattern, BetwayCode.error_msg)
        self.name = raw_code

    def getSite(self) -> Sites:
        return Sites.Betway
    
    def __str__(self) -> str:
        return f'{self.name}'

class BetclicCode(LeagueCode):

    pattern = '\\A\\d{1,8}\\Z'
    error_msg = 'Invalid betclic league code! A betclic league code follows the format:\n `0000`'

    def __init__(self, raw_code: str):
         
        super().__init__(raw_code, BetclicCode.pattern, BetclicCode.error_msg)
        self.id = raw_code

    def getSite(self) -> Sites:
        return Sites.Betclic
    
    def __str__(self) -> str:
        return f'{self.id}'

def LeagueCodesFactory(site: Sites, raw_code: str) -> Optional[LeagueCode]:
    if site == Sites.Bwin:
        return BwinCode(raw_code)
    elif site == Sites.Betano:
        return BetanoCode(raw_code)
    elif site == Sites.Betclic:
        return BetclicCode(raw_code)
    elif site == Sites.Solverde:
        return SolverdeCode(raw_code)
    elif site == Sites.Moosh:
        return MooshCode(raw_code)
    elif site == Sites.Betway:
        return BetwayCode(raw_code)

        