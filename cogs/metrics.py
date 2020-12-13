"""A cog that keeps track of certain chat metrics.
Stores data in it's own collection on MongoDB."""
import discord
from discord.ext import commands, tasks
import datetime
from collections import defaultdict

class Metrics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        db = self.bot.mongo["bot-data"]
        self.cached_message_count = 0
        self.loaded_time = datetime.datetime.now()
        self.cache = defaultdict(lambda: 0)
        self.last_stored_time = None
        self.bot.metrics_collection = self.metrics_collection = db["metrics"]

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        self.cache[message.author.id] += 1
        self.cached_message_count += 1

    @commands.has_guild_permissions(administrator=True)
    @commands.command(name="start-metrics")
    async def start_metrics(self, ctx):
        self.metrics_dump.start()
        await ctx.message.add_reaction("✅")
        embed = discord.Embed(title="Metrics Tracking: Started!", description=f"Time: {self.last_stored_time}", color=discord.Color.green())
        await ctx.send(embed=embed)

    @commands.has_guild_permissions(administrator=True)
    @commands.command(name="stop-metrics")
    async def stop_metrics(self, ctx):
        self.metrics_dump.stop()

        if len(self.cache) != 0:
            self.last_stored_time = datetime.datetime.now()
            insert_doc = {"datetime": self.last_stored_time, counts: self.cache}
            await self.metrics_collection.insert_one(insert_doc)
            self.cache = defaultdict(lambda: 0)
            self.cached_message_count += 1
        
        embed = discord.Embed(title="Metrics Tracking: Stopped", description=f"Time: {self.last_stored_time}", color=discord.Color.red())

    @tasks.loop(hours=1)
    async def metrics_dump(self):
        # add new data hourly to the db and then reset counts and cache
        self.last_stored_time = datetime.datetime.now()

        if len(self.cache) != 0:
            insert_doc = {"datetime": self.last_stored_time, counts: self.cache}
            await self.metrics_collection.insert_one(insert_doc)

        self.cache = defaultdict(lambda: 0)
        self.cached_message_count = 0

    @tasks.loop(hours=24)
    async def metrics_clear(self):
        pass

def setup(bot):
    bot.add_cog(Metrics(bot))

        

        



