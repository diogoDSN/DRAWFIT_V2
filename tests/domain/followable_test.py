import pytest

from drawfit.utils import Sites
from drawfit.domain.followables import Followable

from ..utils import BWIN, BETANO, TEAM1, TEAM1_BWIN_ID, NO_TEAM_ID


@pytest.fixture
def set_id():
    followable = Followable([TEAM1])
    followable.setId(BWIN, TEAM1)
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

    assert followable.isId(BWIN, TEAM1)
    assert not followable.isId(BWIN, NO_TEAM_ID)
    assert not followable.isId(BETANO, TEAM1)

def test_could_be_name(set_id):

    followable = set_id

    assert not followable.couldBeId(BWIN, TEAM1_BWIN_ID)
    assert not followable.couldBeId(BWIN, NO_TEAM_ID)
    assert followable.couldBeId(BETANO, TEAM1_BWIN_ID)
    assert not followable.couldBeId(BETANO, NO_TEAM_ID)

def test_complete():

    followable = Followable([TEAM1])

    for site in Sites:
        followable.setId(site, 'Any Id')
    
    assert followable.complete

def test_add_keywords():

    f1 = Followable()
    f2 = Followable()

    f1.addKeywords(["key1", "key2"])

    assert f1.keywords == ["key1", "key2"]
    assert f2.keywords == []

