from datetime import datetime
from typing import Tuple

class OddSample:

    def __init__(self, game_id: Tuple[str], odd: float, start_time: datetime, sample_time: datetime):
        self._game_id = game_id
        self._odd = odd
        self._start_time = start_time
        self._sample_time = sample_time
    
    @property
    def game_id(self) -> Tuple[str]:
        return self._game_id
    
    @property
    def odd(self) -> float:
        return self._odd
    
    @property
    def start_time(self) -> datetime:
        return self._start_time
     
    @property
    def sample_time(self) -> datetime:
        return self._sample_time

    @property
    def team1_id(self) -> Tuple[str]:
        return (self.game_id[0],)
    
    @property
    def team2_id(self) -> Tuple[str]:
        return (self.game_id[1],)
    
    @property
    def game_name(self) -> str:
        return f'{self.game_id[0]} vs {self.game_id[1]}'
    
    @property
    def team1_name(self) -> str:
        return self.team1_id[0]

    @property
    def team1_name(self) -> str:
        return self.team1_id[1]
    
    def __str__(self) -> str:
        return f'Sample for {self.game_id} with value {self.odd}'
