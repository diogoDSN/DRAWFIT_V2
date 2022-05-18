from datetime import datetime
from typing import Tuple

class OddSample:

    def __init__(self, game_id: Tuple[str], odd: float, start_time: datetime, sample_time: datetime):
        self.game_id = game_id
        self.odd = odd
        self.start_time = start_time
        self.sample_time = sample_time
    
    @property
    def team1_id(self) -> Tuple[str]:
        return (self.game_id[0],)
    
    @property
    def team2_id(self) -> Tuple[str]:
        return (self.game_id[1],)
    
    @property
    def game_name(self) -> str:
        return f'{self.game_id[0]} vs {self.game_id[1]}'