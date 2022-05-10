from datetime import datetime
import re

from typing import List, NoReturn


def convertDate(date: str):
    """
    Returns the datetime objetc corresponding to date.
    date - comes in de format 2022-02-20T17:00:00Z
    Throws ValueError if the date is invalid
    """

    if not re.search('^2\\d{3}-[01]\\d-[0123]\\dT[012]\\d:[012345]\\d:[012345]\\dZ$', date):
        raise ValueError(message="Invalid date format \"" + date + "\"")

    components = list(map(int, re.split('[-,:,T]', date[:-1])))

    return datetime(components[0], components[1], components[2], components[3], components[4], components[5])

def convertMilisecondsEpoch(epochValue: int):
    """
    Returns the datetime objetc corresponding to the given epochTime.
    date - comes in de format 2022-02-20T17:00:00Z
    Throws ValueError if the epoch is invalid
    """
    return datetime.fromtimestamp(epochValue/1000)

class OddSample:

    def __init__(self, game_id: str, odd: int, game_time: datetime, sample_time: datetime, teams: List[str]) -> NoReturn:
        self.game_id = game_id
        self.odd = odd
        self.game_time = game_time
        self.sample_time = sample_time
        self.team1 = teams[0]
        self.team2 = teams[1]
    
    def __str__(self) -> str:
        return f'(Game: {self.game_id}; Value: {self.odd}; GameTime: {self.game_time}; SampleTime: {self.sample_time});'
