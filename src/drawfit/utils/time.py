from datetime import datetime
from pytz import timezone

from drawfit.parameters import TIME_ZONE

def str_dates(date: datetime) -> str:
    return date.strftime(f'%Y-%m-%d\n%H:%M:%S')

def now_lisbon():
    return datetime.now(timezone(TIME_ZONE))

def tz_aware(t: datetime) -> datetime:
    date_in_utc = timezone('UTC').localize(t)

    return date_in_utc.astimezone(timezone(TIME_ZONE))

def to_utc(t: datetime) -> datetime:
    return t.astimezone(timezone('UTC'))
