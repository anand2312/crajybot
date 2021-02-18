import random
import datetime

import discord
from discord.ext import commands, tasks

from secret.constants import *

from utils.embed import CrajyEmbed

from internal.bot import CrajyBot
from internal.enumerations import Table, EmbedType


intents = discord.Intents.default()
intents.members = True    # TO DO: Investigate feature-loss with Member intents disabled
intents.messages = True
bot = CrajyBot(command_prefix=commands.when_mentioned_or("."),
               activity=discord.Activity(type=discord.ActivityType.watching, name="cute panda videos or something."),
               intents=intents,
               owner_id=271586885346918400)

bot.task_loops = dict()    # add all task loops, across cogs to this.

if __name__ == "__main__":
    """To Do: Remove the exception and have this be the main way to run the bot through docker."""
    raise Exception("Use the manage.py interface to run the bot.")
