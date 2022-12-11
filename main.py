import os
import dotenv
import disnake

from disnake.ext import commands
from assets.tools.usercheckers import is_owner

from circleutilitybot import CircleUtility

dotenv.load_dotenv()
print("Fetching bot token...")
token = os.environ.get("BOT_TOKEN")
if token == "":
    print("Please insert a valid discord bot token in the environment file.")
    exit(0)

circleutils = CircleUtility()


@circleutils.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def ping(ctx):
    await ctx.reply(f"🏓 **Pong!** `{round(circleutils.latency * 1000)} ms`", mention_author=False)


@circleutils.slash_command(name="tools_reload")
@commands.check(is_owner)
async def _tools_reload(inter: disnake.GuildCommandInteraction):
    """reloads module loaders (load, unload, reload, restart)"""
    try:
        circleutils.unload_extension("cogs.ModuleLoader")
        circleutils.load_extension("cogs.ModuleLoader")
        await inter.response.send_message("Success reloading **module loaders**.")
    except disnake.ext.commands.ExtensionNotLoaded:
        circleutils.load_extension("cogs.ModuleLoader")
        await inter.response.send_message("Success reloading **module loaders**.")


if __name__ == "__main__":
    try:
        circleutils.run(token)
    except disnake.errors.LoginFailure:
        print("\nImproper/invalid token has been passed, please check your token in the environment file.\n")
