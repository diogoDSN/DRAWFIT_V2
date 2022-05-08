from datetime import datetime

class SiteError(Exception):

    def __init__(self, site_name: str):
        self.site_name = site_name
        self.timestamp = datetime.now()
    
    def error_message(self):
        return f'Error! Couldn\' parse odd data from {self.site_name}. [{self.timestamp}]'