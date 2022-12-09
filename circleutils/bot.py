import os
import sys
import traceback
import dotenv
import disnake

from disnake.ext import commands

from assets.constants.intents import INTENTS
from assets.constants.ignoredmodules import IGNORED_MODULES

dotenv.load_dotenv()


class CircleUtils(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=(["c!", "C!"]),
            intents=INTENTS,
            case_insensitive=True,
            activity=disnake.Game(name="Helping Circle"),
            status="idle",
            owner_id=389034898666553344
        )

        for extension in os.listdir("./cogs"):
            if extension.endswith(".py") and extension[:-3] not in IGNORED_MODULES:
                try:
                    self.load_extension(f"cogs.{extension[:-3]}")
                    print(f"[INFO] Loaded {extension[:-3]}.")
                except:
                    print(f"[INFO] Failed to load {extension}", file=sys.stderr)
                    traceback.print_exc()
        print(f"Ignored modules (disabled on start): {', '.join(IGNORED_MODULES)}")
