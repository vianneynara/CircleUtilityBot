import disnake
import datetime
import asyncio
import random

from disnake.ext import commands

from typing import Any
from assets.methods.time_converters import get_timedelta_epoch
from assets.exceptions import InvalidTargetException
from assets.views import ModerationModal


async def target_check(
        bot: commands.Bot,
        inter: Any,
        target: disnake.Member
):
    if target.id == bot.user.id:
        await inter.response.send_message("Target should not be the bot itself!")
        raise InvalidTargetException()
    elif target.id == inter.author.id:
        await inter.response.send_message("Target should not be yourself!")
        raise InvalidTargetException()
    elif target.guild_permissions.administrator or target.guild_permissions.moderate_members:
        await inter.response.send_message("Target is a moderator!")
        raise InvalidTargetException()

    botmember = inter.guild.get_member(bot.user.id)
    if (
            botmember.top_role.position < target.top_role.position
            or botmember.top_role.position == target.top_role.position
    ):
        await inter.response.send_message("Make sure that I have a higher role than the target!")
        raise InvalidTargetException()


class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="freeze")
    @commands.has_permissions(moderate_members=True)
    async def _freeze(
            self,
            inter: disnake.GuildCommandInteraction,
            target: disnake.Member,
            duration="3h",
            reason="Frozen for no reason."
    ):
        """Freezes(timeouts) a specific member, preventing them from interacting in the server.

        Parameters
        ----------
        target: The member to be frozen.
        duration: The duration of this freeze. (e.g. 1d3h -> 1 day 3 hours, max is 28 days.) Default is 3 hours.
        reason: Action reason.
        """
        try: await target_check(self.bot, inter, target)
        except InvalidTargetException: return
        await inter.response.defer()

        timedelta, epoch = await get_timedelta_epoch(inter, duration)
        await target.timeout(duration=timedelta, reason=reason)
        await inter.edit_original_message(f"<@!{target.id}> **has been frozen until** <t:{int(epoch)}:F>.")

    @commands.message_command(name="quick freeze")
    @commands.has_permissions(moderate_members=True)
    async def _freeze(
            self,
            inter: disnake.GuildCommandInteraction,
            message: disnake.Message,
    ):
        try: await target_check(self.bot, inter, message.author)
        except InvalidTargetException: return
        await inter.response.send_modal(modal=ModerationModal(action="Freezing", duration=True))
        try:
            modal = await self.bot.wait_for(
                "modal_submit",
                check=lambda inter: disnake.ModalInteraction.response.name,
                timeout=300
            )
        except asyncio.TimeoutError:
            return
        duration, reason = modal.text_values["duration"], modal.text_values["reason"]
        timedelta, epoch = await get_timedelta_epoch(inter, duration)
        await message.author.timeout(duration=timedelta, reason=reason)
        await modal.edit_original_message(
            f"<@!{message.author.id}> **has been frozen until** <t:{int(epoch)}:F>."
            f"\nFor: `{reason}`"
        )


def setup(bot):
    bot.add_cog(Moderation(bot))
