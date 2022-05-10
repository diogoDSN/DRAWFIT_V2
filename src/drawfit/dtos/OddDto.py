from datetime import datetime

class OddDto:

    def __init__(self, value: float, date: datetime, game: str):
        self.value = value
        self.date = date
        self.game = game
    
    @property
    def value(self) -> float:
        return self.value

    @property
    def date(self) -> datetime:
        return self.date

    @property
    def game(self) -> str:
        return self.game