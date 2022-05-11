from typing import List, NoReturn

from drawfit.utils import Sites


class Team:

    def __init__(self, name: str, league_name: str):
        
        self.name: str = name
        self.league: str = league_name
        self.active: bool = True

        self.keywords: List[str] = [name]
        self.complete: bool = False

        # Set properties dependent of site
        self.site_names: List[str] = []
        self.considered_names: List[List[str]] = []

        for _ in Sites:
            self.site_names.append(None)
            self.considered_names.append([])
    
    @property
    def name(self) -> str:
        return self.name
    
    def addKeyword(self, new_keyword: str) -> NoReturn:
        self.keywords.append(new_keyword)
    
    def siteName(self, site: Sites) -> str:
        return self.site_names[site.value]

    def setSiteName(self, site: Sites, name: str) -> NoReturn:
        self.site_names[site.value] = name

        if None not in self.site_names:
            self.complete = True
    
    def addConsideredName(self, site: Sites, name: str) -> NoReturn:
        self.considered_names.append(name)

    def removeConsideredName(self, site: Sites, name: str) -> NoReturn:
        self.considered_names.remove(name)
    
    def deactivate(self):
        self.active = False
    
    def activate(self):
        self.active = True
    
    def isTeam(self, site: Sites, team_name: str) -> bool:
        return self.active and team_name == self.site_names[site.value]
    
    def couldBeTeam(self, site: Sites, team_name: str) -> bool:

        if self.complete or not self.active or team_name in self.considered_names[site.value]:
            return False

        if self.site_names[site.value] is None:
            for keyword in self.keywords:
                if keyword in team_name or team_name in keyword:
                    return True
        
        return False

