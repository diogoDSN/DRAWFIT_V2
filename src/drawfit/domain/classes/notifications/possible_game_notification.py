from typing import Tuple

import drawfit.domain as domain

from drawfit.utils import Sites, OddSample

class PossibleGameNotification(domain.PossibleNotification):

    def __init__(self, game: domain.Game, sample: OddSample, site: Sites):
        super().__init__(sample, sample.game_id, site)
        self._game = game
    
    @property
    def followable(self) -> domain.Followable:
        return self._game

    
    def __str__(self):
        return 'PossibleGameNotification'