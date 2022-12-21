from typing import Any

import disnake
from disnake import ui

REASON: dict = {
    "freeze": "Frozen",
    "warn": "Warned",
    "strike": "Striked"
}


class ModerationModal(ui.Modal):
    def __init__(
            self,
            custom_id: str,
            action: str,
            duration: bool = False
    ):
        super().__init__(
            title=action,
            custom_id=custom_id,
            components=[
                ui.TextInput(
                    label="Reason",
                    placeholder="Reason for this action",
                    style=disnake.TextInputStyle.short,
                    max_length=128,
                    custom_id="reason",
                    required=False
                )
            ]
        )
        self.has_duration = duration
        self.action = action
        if duration:
            self.append_component(
                ui.TextInput(
                    label="Duration",
                    placeholder="Default duration is 3 hours (3h)",
                    style=disnake.TextInputStyle.short,
                    max_length=16,
                    custom_id="duration",
                    required=False
                )
            )

    async def callback(self, modal: disnake.ModalInteraction):
        await modal.response.defer()

        if modal.text_values["reason"] == '':
            modal.text_values["reason"] = "No reason provided."

        if self.has_duration:
            if modal.text_values["duration"] == '':
                modal.text_values["duration"] = "3h"
