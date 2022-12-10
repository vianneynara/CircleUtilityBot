import datetime
import re
import disnake

from assets.exceptions import InvalidDurationException, DurationTooLongException
from typing import Any

time_utcnow = disnake.utils.utcnow()


def get_timedelta_epoch(duration: str, restrict=True):
    if duration[0].isalpha() or duration[-1:].isdigit():
        try:
            raise InvalidDurationException("Duration invalid!")
        except disnake.errors.InteractionResponded:
            raise InvalidDurationException("Duration invalid!")

    timedelta = get_timedelta(duration)
    if restrict:
        if timedelta > datetime.timedelta(days=28):
            raise DurationTooLongException
    epoch = (time_utcnow + timedelta).timestamp()
    return timedelta, epoch


def get_timedelta(duration: str):
    duration = duration.lower().replace(" ", "")  # lower the string and remove spaces
    values = {"days": 0, "hours": 0, "minutes": 0, "seconds": 0}
    for k in values.copy():
        try:
            value = re.search("\d+" + k[0], duration).group()  # search for a number that stands next to a certain letter
            values[k] = int(value.replace(k[0], ""))  # extract the number
        except:
            pass  # if the number wasn't found, just leave it with the default value - 0

    return datetime.timedelta(**values)
