import disnake
from disnake import ui


class ModerationModal(ui.Modal):
    def __init__(
            self,
            action: str,
            duration: bool = False
    ):
        super().__init__(
            title=action,
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

    async def callback(self, modal: disnake.ModalInteraction, /):
        await modal.response.defer()
        if self.has_duration:
            if not modal.text_values["duration"]:
                modal.text_values["duration"] = "3h"

            if not modal.text_values["reason"]:
                modal.text_values["reason"] = "Frozen for no reason."
        else:
            if not modal.text_values["reason"]:
                modal.text_values["reason"] = "Frozen for no reason."
