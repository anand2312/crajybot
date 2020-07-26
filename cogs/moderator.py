import discord 
from discord.ext import commands
import random
import asyncio
from pymongo import MongoClient
#do whatever imports you need; I've just done a few which I could think of

client = MongoClient("mongodb://localhost:27017/")
db = client["bot-data"]

economy_collection = db["econ_data"]
rpg_collection = db["rpg_data"]
store_collection = db["store_data"]

channels_available = ["bot-test","botspam-v2","botspam"]

class Moderator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


"""Add commands here as methods of the class. (self will be the first parameter before ctx)
Use decorator ``@commands.command`` instead of ``@bot.command``, any references to ``bot`` from within this code (for like emojis, bot.get_emoji()),
should become ``self.bot``."""
    



def setup(bot):
    bot.add_cog(Moderator(bot))