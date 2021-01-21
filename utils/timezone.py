
import pytz
from datetime import timedelta

BOT_TZ = pytz.timezone("Asia/Dubai")

def get_timedelta(arg: str) -> timedelta:
    """Converts a string of time for eg: 5h -> into an equivalent timedelta object."""
    time_, units = [], []
    arg = arg.lower()

    unit_mapping = {
        "h": "hours", "hour": "hours", 
        "m": "minutes", "minute": "minutes",
        "s": "seconds", "second": "seconds",
        "d": "days", "day": "days",
        "month": "months",     # m already assigned for minutes
        "year": "years"
    }

    for i in arg:
        if i.isdigit():
            time_.append(int(i))
        else:
            units.append(unit_mapping[i])

    return timedelta(**dict(zip(time_, units)))