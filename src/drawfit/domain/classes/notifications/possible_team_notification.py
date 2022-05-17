from typing import Tuple

import drawfit.domain as domain

from drawfit.utils import Sites, OddSample

class PossibleTeamNotification(domain.PossibleNotification):

    def __init__(self, team: domain.Team, sample: OddSample, team_id: Tuple[str], site: Sites):
        super().__init__(sample, team_id, site)
        self._team = team
    
    @property
    def followable(self) -> domain.Followable:
        return self._team

    def __str__(self):
        return 'PossibleTeamNotification'