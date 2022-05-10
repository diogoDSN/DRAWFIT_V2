from domain.classes.Sites import Sites

class OddNotification:

    def __init__(self, game_name: str, value: int, timestamp: datetime, site: Sites):

        self.game_name: str = game_name
        self.value: int = possible_name
        self.timestamp: datetime = timestamp
        self.site: Sites = site

    def __str__(self):
        return f''