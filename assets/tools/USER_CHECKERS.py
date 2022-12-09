import disnake
from assets.CONFIG_CONSTANTS import OWNER_ID
from typing import Any


def is_owner(ctx: Any[disnake.Interaction | disnake.GuildCommandInteraction]):
    return ctx.author.id == OWNER_ID
