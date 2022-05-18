import re

from drawfit.utils.league_codes.league_code_error import LeagueCodeError

class LeagueCode:
    pass


class BwinCode(LeagueCode):

    pattern = '\\A\\d{4},\\d{5,7}\\Z'
    error_msg = 'Invalid bwin league code! A bwin league code follows the format:\n `0000,000000`'

    def __init__(self, raw_code: str):
        
        if not re.search(BwinLeagueCode.pattern, raw_code):
            raise LeagueCodeError(BwinLeagueCode.error_msg)
        
        self.region_id, self.competition_id = raw_code.split(',')
        