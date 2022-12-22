import disnake
from disnake.ext import commands

from assets.constants.disabled_commands import DISABLED_COMMANDS


def is_command_enabled():
    async def predicate(inter: disnake.ApplicationCommandInteraction):
        if inter.data.name.lower() not in DISABLED_COMMANDS:
            return True

        await inter.response.send_message("This command is disabled on default.", ephemeral=True)
        return False

    return commands.check(predicate)
