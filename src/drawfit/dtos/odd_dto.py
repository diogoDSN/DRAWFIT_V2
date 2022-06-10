from __future__ import annotations

from datetime import datetime

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from drawfit.domain.odd import Odd

class OddDto:

    def __init__(self, odd: Odd):
        self._value: float = odd.value
        self._date: datetime = odd.date
    
    @property
    def value(self) -> float:
        return self._value

    @property
    def date(self) -> datetime:
        return self._date