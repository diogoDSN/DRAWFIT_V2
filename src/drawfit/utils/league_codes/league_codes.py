import re
from abc import abstractmethod

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

    pattern = '\\A\\d{1,2},\\d{5,7}\\Z'
    error_msg = 'Invalid bwin league code! A bwin league code follows the format:\n `0000,000000`'

    def __init__(self, raw_code: str):
        
        super().__init__(raw_code, BwinCode.pattern, BwinCode.error_msg)
        self.region_id, self.competition_id = raw_code.split(',')

    def getSite(self) -> Sites:
        return Sites.Bwin

class BetanoCode(LeagueCode):

    pattern = '\\A\\d{4,6}\\Z'
    error_msg = 'Invalid betano league code! A betano league code follows the format:\n `00000`'

    def __init__(self, raw_code: str):
        
        super().__init__(raw_code, BetanoCode.pattern, BetanoCode.error_msg)
        self.id = raw_code

    def getSite(self) -> Sites:
        return Sites.Betano
        