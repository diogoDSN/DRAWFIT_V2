from __future__ import annotations

from datetime import datetime, timedelta
from typing import NoReturn

import drawfit.domain.followables as f

class Odd:

    def __init__(self, value: float, date: datetime, game: f.Game) -> NoReturn:
        self._value: float = value
        self._date: datetime = date
        self._game = game

    @property
    def value(self) -> float:
        return self._value

    @property
    def date(self) -> datetime:
        return self._date
    
    @property
    def hours_left(self) -> float:
        return self._game.hoursLeft(time=self.date)

    def __eq__(self, o):
        if o.__class__ == self.__class__:
            return self.value == o.value and self.date == o.date

        return False
    
    def __str__(self) -> str:
        return f'Odd: {self.value}; Date: {self.date}'
