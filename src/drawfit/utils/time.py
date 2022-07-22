from datetime import datetime
from pytz import timezone

from drawfit.parameters import TIME_ZONE

def str_dates(date: datetime) -> str:
    return date.strftime(f'%Y-%m-%d\n%H:%M:%S')

def now_lisbon():
    return datetime.now(timezone(TIME_ZONE))