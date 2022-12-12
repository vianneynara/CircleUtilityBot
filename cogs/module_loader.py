import os
import disnake
from disnake.ext import commands

from assets.tools.user_checkers import is_owner
from assets.constants.colors import *

extensions_list = []
for file in os.listdir("./cogs"):
    if file.endswith(".py"):
        extensions_list.append(file[:-3])


class ModuleLoader(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="module", invoke_without_command=True)
    @commands.check(is_owner)
    async def _module(self, inter: disnake.GuildCommandInteraction):
        pass

    @_module.sub_command(name="load")
    async def _module_load(
            self,
            inter: disnake.GuildCommandInteraction,
            module: commands.option_enum(choices=extensions_list)
    ):
        """loads a module

        Parameters
        ----------
        module: module to be loaded
        """
        self.bot.load_extension(f"cogs.{module}")
        print(f"[INFO] Loaded {module[:-3]}.")
        await inter.response.send_message(f"**{module}** has been loaded.")

    @_module.sub_command(name="unload")
    async def _module_unload(
            self,
            inter: disnake.GuildCommandInteraction,
            module: commands.option_enum(choices=extensions_list)
    ):
        """unloads a module

        Parameters
        ----------
        module: module to be unloaded
        """
        self.bot.unload_extension(f"cogs.{module}")
        print(f"[INFO] Unloaded {module[:-3]}.")
        await inter.response.send_message(f"**{module}** has been unloaded.")

    @_module.sub_command(name="reload")
    async def _module_reload(
            self,
            inter: disnake.GuildCommandInteraction,
            module: commands.option_enum(choices=extensions_list)
    ):
        """reloads a module

        Parameters
        ----------
        module: module to be reloaded
        """
        self.bot.unload_extension(f"cogs.{module}")
        self.bot.load_extension(f"cogs.{module}")
        print(f"[INFO] Reloaded {module[:-3]}.")
        await inter.response.send_message(f"**{module}** has been reloaded.")

    @_module.sub_command(name="restart")
    async def _module_restart(self, inter: disnake.GuildCommandInteraction):
        """reloads every loaded and loads unloaded modules."""
        await inter.response.send_message("Reloading all modules...")
        for file in os.listdir("./cogs"):
            if file.endswith(".py"):
                try:
                    self.bot.unload_extension(f"cogs.{file[:-3]}")
                    self.bot.load_extension(f"cogs.{file[:-3]}")
                    print(f"[INFO] Reloaded {file[:-3]}.")
                except disnake.ext.commands.errors.ExtensionNotLoaded:
                    self.bot.load_extension(f"cogs.{file[:-3]}")
                    print(f"[INFO] Loaded {file[:-3]}.")
        await inter.edit_original_message("All modules have been reloaded.")
        print("I have reloaded all extensions.")

    @_module.sub_command(name="list")
    async def _module_list(self, inter: disnake.GuildCommandInteraction):
        """list all available modules in cogs directory"""
        await inter.response.defer()
        modules = [i[:-3] for i in os.listdir("./cogs") if i.endswith(".py")]
        enabled, disabled = [], []
        e_count, d_count = 0, 0

        for module in modules:
            try:
                self.bot.unload_extension(f"cogs.{module}")
            except commands.ExtensionNotLoaded:
                d_count += 1
                disabled.append(f"{d_count:{' '}{'>'}{2}} " + f"{module:{' '}{'<'}{20}} ")

            else:
                e_count += 1
                self.bot.load_extension(f"cogs.{module}")
                enabled.append(f"{e_count:{' '}{'>'}{2}} " + f"{module:{' '}{'<'}{20}} ")

        embed = disnake.Embed(
            title=f"List of available modules [`{len(modules)}`]",
            color=DISCORD_DARKGREY
        )
        if len(enabled) > len(disabled):
            for i in range(0, len(enabled) - len(disabled)): disabled.append(" ")
        else:
            for i in range(0, len(disabled) - len(enabled)): enabled.append(" ")

        if enabled: embed.add_field(name=f"[`🟩`] Enabled", value="```" + '\n'.join(enabled) + "```")
        if disabled:
            embed.add_field(name=f"[`🟥`] Disabled", value="```" + '\n'.join(disabled) + "```")
        await inter.edit_original_message(embed=embed)


def setup(bot):
    bot.add_cog(ModuleLoader(bot))
