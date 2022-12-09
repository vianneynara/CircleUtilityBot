import os
import disnake
from disnake.ext import commands


class Preparations(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # empty


def setup(bot):
    bot.add_cog(Preparations(bot))
