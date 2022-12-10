import datetime
import re
import disnake

from assets.exceptions import InvalidDurationException
from typing import Any

time_utcnow = disnake.utils.utcnow()


async def get_timedelta_epoch(inter: Any, duration: str, restrict=True):
    try: await check_duration(inter, duration)
    except InvalidDurationException: return

    timedelta = get_timedelta(duration)
    if restrict:
        if timedelta > datetime.timedelta(days=28):
            return await inter.response.send_message(
                "Duration is too long, longest freeze time is `28` days.",
                ephemeral=True,
            )
    epoch = (time_utcnow + timedelta).timestamp()
    return timedelta, epoch


async def check_duration(inter: Any, duration: str):
    if duration[0].isalpha() or duration[-1:].isdigit():
        message = "Duration conversion failed! Please use the correct duration format! (e.g. 4h30m)"
        try:
            await inter.response.send_message(message)
            raise InvalidDurationException("Duration invalid!")
        except disnake.errors.InteractionResponded:
            await inter.edit_original_message(message)
            raise InvalidDurationException("Duration invalid!")


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
