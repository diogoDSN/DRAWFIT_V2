from domain.Game import Game

from datetime import datetime

class Odd:

    def __init__(self, value: float, date: datetime, game: Game):
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
    def game(self) -> Game:
        return self.game
