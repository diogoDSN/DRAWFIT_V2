from datetime import datetime

class OddDto:

    def __init__(self, value: float, date: datetime):
        self.value = value
        self.date = date
    
    @property
    def value(self) -> float:
        return self.value

    @property
    def date(self) -> datetime:
        return self.date