import disnake

from assets.constants.owner_id import OWNER_ID
from typing import Any


def is_owner(context: Any) -> bool:
    return context.author.id == OWNER_ID


def is_moderator(context: Any) -> bool:
    return context.author.guild_permissions.moderate_members


def is_admin(context: Any) -> bool:
    return context.author.guild_permissions.administrator
