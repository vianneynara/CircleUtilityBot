import os
import sys
import traceback
import dotenv
import disnake

from disnake.ext import commands
from disnake.ext.commands import Bot

from assets.constants.INTENTS import INTENTS
from assets.constants.IGNORED_MODULES import IGNORED_MODULES
from assets.tools.USER_CHECKERS import is_owner


def start_bot(token: str):
    if token == "":
        print("Please insert a valid discord bot token in the environment file.")
        exit(0)

    bot = Bot(
        command_prefix=(["c!", "C!"]),
        intents=INTENTS,
        case_insensitive=True,
        activity=disnake.Game(name="Helping Circle"),
        status="idle"
    )

    for extension in os.listdir("./cogs"):
        if extension.endswith(".py") and extension[:-3] not in IGNORED_MODULES:
            try:
                bot.load_extension(f"cogs.{extension[:-3]}")
                print(f"[INFO] Loaded {extension[:-3]}.")
            except:
                print(f"[INFO] Failed to load {extension}", file=sys.stderr)
                traceback.print_exc()
    print(f"Ignored modules (disabled on start): {', '.join(IGNORED_MODULES)}")

    """BASIC COMMANDS"""
    @bot.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ping(ctx):
        await ctx.reply(f"🏓 **Pong!** `{round(bot.latency * 1000)} ms`", mention_author=False)

    """MODULE CONFIGS"""
    @bot.slash_command(name="tools_reload")
    @commands.check(is_owner)
    async def _tools_reload(inter: disnake.GuildCommandInteraction):
        """reloads module loaders (load, unload, reload, restart)"""
        try:
            bot.unload_extension("cogs.ModuleLoader")
            bot.load_extension("cogs.ModuleLoader")
            await inter.response.send_message("Success reloading **module loaders**.")
        except:
            bot.load_extension("cogs.ModuleLoader")
            await inter.response.send_message("Success reloading **module loaders**.")

    bot.run(token)


if __name__ == "__main__":
    dotenv.load_dotenv()
    print("Fetching bot token...")
    TOKEN = os.environ.get("BOT_TOKEN")
    start_bot(TOKEN)