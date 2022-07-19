from datetime import datetime
from pytz import timezone

from drawfit.parameters import TIME_ZONE

def now_lisbon():
    return datetime.now(timezone(TIME_ZONE))