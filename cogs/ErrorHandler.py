import disnake
import asyncio

from disnake.ext import commands

datetime_now = disnake.utils.utcnow()


def get_cooldown(error: commands.errors.CommandOnCooldown):
    seconds, minutes, hours = (
        round(divmod(error.retry_after, 60)),
        round(divmod(error.retry_after, 3600)),
        round(round(divmod(error.retry_after, 3600)) % 24)
    )
    return (
        f"Command under cooldown, please try again in "
        f"{f'**{round(hours)}** hours ' if round(hours) > 0 else ''}"
        f"{f'**{round(minutes)}** minutes ' if round(minutes) > 0 else ''}"
        f"{f'**{round(seconds)}** seconds' if round(seconds) > 0 else ''}."
    )


class ErrorHandler(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_slash_command_error(
            self,
            inter: disnake.ApplicationCommandInteraction,
            error: Exception
    ) -> None:
        error = getattr(error, "original", error)  # gets the actual disnake error

        if isinstance(error, commands.errors.CheckFailure):
            return

        if isinstance(error, commands.MissingPermissions):
            message = f"You are missing `{', '.join(error.missing_permissions)}` permission to run this command."
            await inter.response.send_message(message, ephemeral=True)

        elif isinstance(error, commands.errors.MemberNotFound):
            message = f"Member not found."
            await inter.response.send_message(message, ephemeral=True)

        elif isinstance(error, commands.errors.UserNotFound):
            message = f"User not found."
            await inter.response.send_message(message, ephemeral=True)

        elif isinstance(error, commands.errors.MissingRole):
            message = f"You are missing <@&{error.missing_role}> to execute this command."
            await inter.response.send_message(message, ephemeral=True)

        elif isinstance(error, commands.errors.CheckFailure):
            message = f"Error validating command, ask the developer for more information."
            await inter.response.send_message(message, ephemeral=True)

        elif isinstance(error, commands.errors.CommandOnCooldown):
            await inter.response.send_message(get_cooldown(error), ephemeral=True)

        elif isinstance(error, commands.ExtensionNotFound):
            message = f"Extension {error.name.partition('.')[2]} not found."
            await inter.followup.send(message, ephemeral=True)
            await inter.delete_original_message()

        elif isinstance(error, commands.ExtensionAlreadyLoaded):
            message = f"Extension {error.name.partition('.')[2]} already loaded."
            await inter.followup.send(message, ephemeral=True)
            await inter.delete_original_message()

        elif isinstance(error, commands.ExtensionNotLoaded):
            message = f"Extension {error.name.partition('.')[2]} not loaded, please load it first."
            await inter.followup.send(message, ephemeral=True)
            await inter.delete_original_message()

        elif isinstance(error, commands.ExtensionError):
            message = f"Extension {error.name.partition('.')[2]} has an error, " \
                      f"please ask the developer to investigate." \
                      f"\n```fix\n{error.__context__[:3000]}{'...' if len(str(error.__context__)) > 3000 else ''}```"
            await inter.followup.send(message, ephemeral=True)
            await inter.delete_original_message()

        elif isinstance(error, commands.ExtensionError):
            message = f"Extension {error.name.partition('.')[2]} has failed to load, " \
                      f"please ask the developer to investigate." \
                      f"\n```fix\n{error.__context__[:3000]}{'...' if len(str(error.__context__)) > 3000 else ''}```"
            await inter.followup.send(message, ephemeral=True)
            await inter.delete_original_message()

        else:
            # this will be executed if the error is not handled above
            message = f"An unhandled error has occurred, please ask the developer to investigate." \
                      f"\n```fix\n{error}```"
            await inter.followup.send(message)
            raise error

    @commands.Cog.listener()
    async def on_message_command_error(
            self,
            inter: disnake.ApplicationCommandInteraction,
            error: Exception
    ) -> None:
        error = getattr(error, "original", error)  # gets the actual disnake error

        if isinstance(error, commands.errors.CheckFailure):
            return

        if isinstance(error, commands.MissingPermissions):
            message = f"You are missing `{', '.join(error.missing_permissions)}` permission to run this command."
            await inter.response.send_message(message, ephemeral=True)

        elif isinstance(error, commands.errors.MemberNotFound):
            message = f"Member not found."
            await inter.response.send_message(message, ephemeral=True)

        elif isinstance(error, commands.errors.UserNotFound):
            message = f"User not found."
            await inter.response.send_message(message, ephemeral=True)

        elif isinstance(error, commands.errors.MissingRole):
            message = f"You are missing <@&{error.missing_role}> to execute this command."
            await inter.response.send_message(message, ephemeral=True)

        elif isinstance(error, commands.errors.CheckFailure):
            message = f"Error validating command, ask the developer for more information."
            await inter.response.send_message(message, ephemeral=True)

        elif isinstance(error, commands.errors.CommandOnCooldown):
            await inter.response.send_message(get_cooldown(error), ephemeral=True)

        else:
            # this will be executed if the error is not handled above
            message = f"An unhandled error has occurred, please ask the developer to investigate." \
                      f"\n```fix\n{error}```"
            await inter.followup.send(message)
            raise error


def setup(bot: commands.Bot):
    bot.add_cog(ErrorHandler(bot))
