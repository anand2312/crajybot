import datetime
import random
import logging
import os

import discord
from discord.ext import commands, tasks

from secret.constants import *

from utils.embed import CrajyEmbed

from internal.bot import CrajyBot
from internal.enumerations import Table, EmbedType


intents = discord.Intents.default()
intents.members = True  # TO DO: Investigate feature-loss with Member intents disabled
intents.messages = True
bot = CrajyBot(
    command_prefix=commands.when_mentioned_or("."),
    activity=discord.Activity(
        type=discord.ActivityType.watching, name="cute panda videos or something."
    ),
    intents=intents,
    owner_id=271586885346918400,
)

if __name__ == "__main__":
    if os.environ.get("PRODUCTION"):
        bot.logger.info(f"Began Loading Extensions")
        for ext in os.listdir("./exts"):
            bot.load_extension(f"exts.{ext}")
            bot.logger.info(f"Loaded Extension: {ext}")
        bot.load_extension("jishaku")
        bot.logger.info(f"Finished Loading Extensions.")

        for loop in bot.task_loops.values():
            loop.start()

    else:
        raise RuntimeError("Use the manage.py interface to run code while debugging.")

    bot.run(TOKEN)
