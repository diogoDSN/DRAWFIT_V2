from datetime import datetime
from typing import NoReturn

class Odd:

    def __init__(self, value: float, date: datetime) -> NoReturn:
        self._value: float = value
        self._date: datetime = date

    @property
    def value(self) -> float:
        return self._value

    @property
    def date(self) -> datetime:
        return self._date

    def __eq__(self, o):
        if o.__class__ == self.__class__:
            return self.value == o.value and self.date == o.date

        return False
    
    def __str__(self) -> str:
        return f'Odd: {self.value}; Date: {self.date}'
