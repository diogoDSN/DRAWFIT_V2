from datetime import datetime
from pytz import timezone

def now_lisbon():
    return datetime.now(timezone('Europe/Lisbon'))