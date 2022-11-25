from datetime import datetime
from pytz import timezone

from drawfit.parameters import TIME_ZONE

def str_dates(date: datetime) -> str:
    return date.strftime(f'%Y-%m-%d\n%H:%M:%S')

def now_lisbon():
    return datetime.now(timezone(TIME_ZONE))

def tz_aware(t: datetime) -> datetime:
    tz = timezone(TIME_ZONE)
    return tz.localize(t)

def to_utc(t: datetime) -> datetime:
    return t.astimezone(timezone('UTC'))
