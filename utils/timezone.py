from datetime import timedelta
from itertools import groupby
import pytz

BOT_TZ = pytz.timezone("Asia/Dubai")


def get_timedelta(arg: str) -> timedelta:
    """Converts a string of time for eg: 5h -> into an equivalent timedelta object."""
    arg = arg.lower()
    amts, units = [], []

    unit_mapping = {
        "h": "hours",
        "hour": "hours",
        "m": "minutes",
        "minute": "minutes",
        "s": "seconds",
        "second": "seconds",
        "d": "days",
        "day": "days",
        "month": "months",  # m already assigned for minutes
        "year": "years",
    }

    grouped = groupby(arg, key=str.isdigit)

    for key, group in grouped:
        if key:  # means isdigit returned true, meaning they are numbers
            amts.append(int("".join(group)))
        else:
            units.append(
                unit_mapping["".join(group)]
            )  # convert h -> hours, m -> minutes and so on

    return timedelta(**dict(zip(units, amts)))
