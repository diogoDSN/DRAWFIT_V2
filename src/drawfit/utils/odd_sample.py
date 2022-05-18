from datetime import datetime
from typing import Tuple

class OddSample:

    def __init__(self, game_id: Tuple[str], odd: float, start_time: datetime, sample_time: datetime):
        self.game_id = game_id
        self.odd = odd
        self.start_time = start_time
        self.sample_time = sample_time