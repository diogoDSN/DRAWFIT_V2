import pytest

from drawfit.utils import Sites
from drawfit.domain.followables import Followable

from ..utils import SITE1, SITE2, TEAM1, TEAM1_ID, NO_TEAM_ID


@pytest.fixture
def set_id():
    followable = Followable([TEAM1])
    followable.setId(SITE1, TEAM1)
    return followable

def test_followable_constructor():
    followable =  Followable([TEAM1])
    assert followable.keywords == [TEAM1]
    assert followable.considered == {site: [] for site in Sites}
    assert followable.ids == {site: None for site in Sites}
    assert followable.complete == False

    with pytest.raises(AttributeError):
        followable.keywords = None
    with pytest.raises(AttributeError):
        followable.considered = None
    with pytest.raises(AttributeError):
        followable.ids = None
    with pytest.raises(AttributeError):
        followable.complete = None

def test_is_name(set_id):

    followable = set_id

    assert followable.isId(SITE1, TEAM1)
    assert not followable.isId(SITE1, NO_TEAM_ID)
    assert not followable.isId(SITE2, TEAM1)

def test_could_be_name(set_id):

    followable = set_id

    assert not followable.couldBeId(SITE1, TEAM1_ID)
    assert not followable.couldBeId(SITE1, NO_TEAM_ID)
    assert followable.couldBeId(SITE2, TEAM1_ID)
    assert not followable.couldBeId(SITE2, NO_TEAM_ID)

def test_complete():

    followable = Followable([TEAM1])

    for site in Sites:
        followable.setId(site, 'Any Id')
    
    assert followable.complete



