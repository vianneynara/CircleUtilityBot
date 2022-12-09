from assets.constants.ownerid import OWNER_ID
from typing import Any


def is_owner(context: Any) -> bool:
    return context.author.id == OWNER_ID
