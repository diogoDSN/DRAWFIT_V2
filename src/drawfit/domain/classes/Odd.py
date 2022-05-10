from datetime import datetime
from typing import NoReturn

class Odd:

    def __init__(self, value: float, date: datetime) -> NoReturn:
        self.value = value
        self.date = date
    
    @property
    def value(self) -> float:
        return self._value
    
    @value.setter
    def value(self, value: float):
        self._value = value

    @property
    def date(self) -> datetime:
        return self._date
    
    @date.setter
    def date(self, date: datetime):
        self._date = date
