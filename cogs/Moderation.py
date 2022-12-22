import typing
import traceback

import disnake
import datetime
import asyncio
import random

from disnake.ext import commands

from typing import Any
from assets.methods.time_converters import get_timedelta_epoch
from assets.exceptions import InvalidTargetException, InvalidDurationException, DurationTooLongException, RequiredParameterMissingException
from assets.tools.user_checkers import is_owner
from assets.views import ModerationModal


async def target_check(
        bot: commands.Bot,
        inter: Any,
        target: disnake.Member,
        is_modal: bool = False
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
    else:
        if not is_modal: await inter.response.defer()


ACTION_TYPES = {
    "kick": "kicked",
    "ban": "banned",
    "freeze": "frozen"
}


async def inform_target(inter: disnake.GuildCommandInteraction, target: disnake.Member, reason: str, action: str, epoch: float = None):
    if action == "freeze":
        if epoch is None:
            raise RequiredParameterMissingException('Parameter "epoch" unfilled!')
        try:
            await target.send(f"You have been {ACTION_TYPES.get(action)} in **{inter.guild.name}** `for` __{reason}__. "
                              f"\nYou will be able to communicate again at <t:{int(epoch)}:F>")
        except disnake.Forbidden:
            await inter.followup.send("User has their DM closed, hence the action was not informed.", ephemeral=True)
    else:
        try:
            await target.send(f"You have been {ACTION_TYPES.get(action)} from **{inter.guild.name}** `for` __{reason}__")
        except disnake.Forbidden:
            await inter.followup.send("User has their DM closed, hence the action was not informed.", ephemeral=True)


class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="freeze")
    @commands.has_permissions(moderate_members=True)
    async def s_freeze(
            self,
            inter: disnake.GuildCommandInteraction,
            target: disnake.Member,
            duration="3h",
            reason="No reason provided."
    ):
        """Prevents a member from interacting in the server.

        Parameters
        ----------
        inter: Interaction.
        target: The member to be frozen.
        duration: The duration of this freeze. (e.g. 1d3h -> 1 day 3 hours, max is 28 days.) Default is 3 hours.
        reason: Action reason.
        """
        try:
            await target_check(self.bot, inter, target)
        except InvalidTargetException:
            return

        try:
            timedelta, epoch = get_timedelta_epoch(duration)
        except InvalidDurationException:
            return await inter.edit_original_message(f"Invalid duration format inserted!")
        except DurationTooLongException:
            return await inter.edit_original_message(f"Duration is too long! Maximum value should be `28` days.")

        await target.timeout(duration=timedelta, reason=reason)
        await inter.edit_original_message(
            f"<@!{target.id}> **has been frozen until** <t:{int(epoch)}:F>."
            f"\n`for:` {reason}"
        )

        await inform_target(inter, target, reason, inter.application_command.name, epoch)

    # @commands.message_command(name="Quick freeze")
    # @commands.has_permissions(moderate_members=True)
    async def m_freeze(
            self,
            inter: disnake.GuildCommandInteraction,
            message: disnake.Message,
    ):
        """Prevents a member from interacting in the server.

        Parameters
        ----------
        inter: Interaction.
        target: The member to be frozen.
        duration: The duration of this freeze. (e.g. 1d3h -> 1 day 3 hours, max is 28 days.) Default is 3 hours.
        reason: Action reason.
        """
        try:
            await target_check(self.bot, inter, message.author, is_modal=True)
        except InvalidTargetException:
            return

        custom_id = f"moderation-modal-{inter.author.id}"
        await inter.response.send_modal(modal=ModerationModal(custom_id=custom_id, action="freeze", duration=True))
        try:
            modal = await self.bot.wait_for(
                "modal_submit",
                check=lambda mod_inter: mod_inter.author.id == inter.author.id and mod_inter.custom_id == custom_id,
                timeout=30
            )
            await modal.edit_original_message(f"Gathering modal inputs...")
        except asyncio.TimeoutError:
            return
        duration, reason = modal.text_values["duration"], modal.text_values["reason"]

        try:
            timedelta, epoch = get_timedelta_epoch(duration)
        except InvalidDurationException:
            return await modal.edit_original_message(f"Invalid duration format inserted!")
        except DurationTooLongException:
            return await modal.edit_original_message(f"Duration is too long! Maximum value should be `28` days.")

        await message.author.timeout(duration=timedelta, reason=reason)
        await modal.edit_original_message(
            f"<@!{message.author.id}> **has been frozen until** <t:{int(epoch)}:F>."
            f"\n`for:` __{reason}__"
        )

    @commands.slash_command(name="unfreeze")
    @commands.has_permissions(moderate_members=True)
    async def s_unfreeze(
            self,
            inter: disnake.GuildCommandInteraction,
            target: disnake.Member
    ):
        """Release a member from server timeout.

        Parameters
        ----------
        inter: Interaction.
        target: The member to be frozen.
        """
        await inter.response.defer()
        if target.current_timeout is None:
            await inter.edit_original_message(f"User is not under timeout.")
        else:
            await target.timeout(duration=0)
            await inter.edit_original_message(f"<@!{target.id}> has been released from timeout.")

    @commands.slash_command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def s_kick(
            self,
            inter: disnake.GuildCommandInteraction,
            target: disnake.Member,
            reason: str = "No reason provided."
    ):
        """Kicks a member from the server.

        Parameters
        ----------
        inter: Interaction.
        target: The member to be kicked.
        reason: Action reason.
        """
        try:
            await target_check(self.bot, inter, target)
        except InvalidTargetException:
            return

        await inform_target(inter, target, reason, inter.application_command.name)

        await target.kick(reason=reason)
        await inter.edit_original_message(
            f"<@!{target.id}> **has been kicked**."
            f"\n`for:` __{reason}__"
        )

    @commands.slash_command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def s_ban(
            self,
            inter: disnake.GuildCommandInteraction,
            target: disnake.Member,
            reason: str = "No reason provided.",
            delete: commands.option_enum(
                {
                    "Don't delete chats from this member": "0",
                    "Chats 1 days before": "1",
                    "Chats 3 days before": "3",
                    "Chats 7 days before": "7",
                }
            ) = "0"
    ):
        """Bans a member from the server.

        Parameters
        ----------
        inter: Interaction.
        target: The member to be banned.
        reason: Action reason.
        delete: Delete chats sent by member.
        """
        try:
            await target_check(self.bot, inter, target)
        except InvalidTargetException:
            return

        await inform_target(inter, target, reason, inter.application_command.name)

        int(delete)
        await target.ban(reason=reason, delete_message_days=delete)
        await inter.edit_original_message(
            f"<@!{target.id}> **has been banned**."
            f"\n`for:` __{reason}__"
        )
        if delete != 0:
            await inter.followup.send(f"Chats sent {delete} day(s) before has also been removed.", ephemeral=True)

    @commands.slash_command(name="unban")
    @commands.has_permissions(ban_members=True)
    async def s_unban(
            self,
            inter: disnake.GuildCommandInteraction,
            target: str,
            reason: str = "No reason provided."
    ):
        """Unbans a member in the server.

        Parameters
        ----------
        inter: Interaction.
        target: The member id to be unbanned.
        reason: Action reason.
        """
        await inter.response.defer()

        target = await self.bot.get_or_fetch_user(int(target))
        if target is None:
            return await inter.edit_original_message("User not found!")

        banned_list = await inter.guild.bans().flatten()
        for banned in banned_list:
            if banned.user.id == target.id:
                await inter.guild.unban(target, reason=reason)
                return await inter.edit_original_message(f"<@!{target.id}> has been unbanned.")

        await inter.edit_original_message("User is not banned from this guild.")

    @commands.slash_command(name="test")
    @commands.check(is_owner)
    async def testing_something(self, inter: disnake.GuildCommandInteraction):
        await inter.response.defer()
        await inter.edit_original_message("User not found!")
        await inter.followup.send("Hey!", ephemeral=True)


def setup(bot):
    bot.add_cog(Moderation(bot))
