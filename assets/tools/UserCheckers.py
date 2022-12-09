import disnake
from assets.OwnerDiscordID import OWNER_ID
from typing import Any


def is_owner(context: Any) -> bool:
    return context.author.id == OWNER_ID
