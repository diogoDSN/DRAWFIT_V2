class LeagueCodeError(Exception):

    def __init__(self, message: str):
        self.error_message = message