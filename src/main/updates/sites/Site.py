from abc import abstractmethod


class Site:

    def __init__(self):
        self.last_odds = {}

    @abstractmethod
    def updateOdds():
        pass


