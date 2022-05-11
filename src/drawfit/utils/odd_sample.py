from datetime import datetime
from typing import List, NoReturn

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
