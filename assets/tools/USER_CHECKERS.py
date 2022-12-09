import disnake
from assets.CONFIG_CONSTANTS import OWNER_ID
from typing import Any


def is_owner(context: Any) -> bool:
    return context.author.id == OWNER_ID
