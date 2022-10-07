from datetime import datetime
from drawfit.utils import now_lisbon

class SiteError(Exception):

    def __init__(self, site_name: str):
        self.site_name = site_name
        self.timestamp = now_lisbon()
    
    def error_message(self):
        return f'Error! Couldn\' parse odd data from {self.site_name}. [{self.timestamp}]'