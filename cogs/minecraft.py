"""Helper functions to help play minecraft with the homies.
Note: These commands depend on resources from Google Cloud Platform
    - 1 N1 VM on Compute Engine
    - 2 Cloud Functions
    - Extra Storage buckets for backing up world data

The workflow is:
    > start/stop server triggered from chat
    > this makes a GET request to a URL - this URL is a trigger for the Cloud Function set up on GCP
    > The Cloud Function triggers the VM to start up/shut down
    > Saved startup/shutdown batch scripts run automatically, running the Minecraft server.

Follow https://cloud.google.com/solutions/gaming/minecraft-server this tutorial to setup the VM, server and batch scripts.
You can try using https://wideops.com/brick-by-brick-learn-gcp-by-setting-up-a-kid-controllable-minecraft-server/ this for the Cloud Functions.

No further documentation will be provided for these commands."""

import discord
from discord.ext import commands

import datetime
import time

from secret.TOKEN import START_LINK, STOP_LINK
from utils.timezone import BOT_TZ

class Minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.running = False

        self.init_time = 0
        
        self.embed = discord.Embed(title="Minecraft Server")
        self.embed.set_thumbnail(url="https://media.discordapp.net/attachments/757877755395309609/779682985163227146/apps.png?width=158&height=158")
        self.embed.set_footer(text="Patience. Don't spam start/stopserver command for sometime. Servers take some time to boot up and shutdown.")

    @commands.cooldown(1, 600, commands.BucketType.guild)
    @commands.command(name="start-server", aliases=["startserver"])
    async def start_server(self, ctx, override: str=False):
        if override != "--override":
            if self.running:
                ctx.command.reset_cooldown(ctx)
                return await ctx.send("Server already running! IP: 35.241.144.6")
            cur_time = time.time()
            diff = (cur_time - self.init_time) // 60
            if diff < 6:          # applies a 6 minute cooldown on startup command after a shutdown
                ctx.command.reset_cooldown(ctx)
                return await ctx.send(f"You're trying to start the server back up too quick. Time since last shutdown sequence ~{diff} mins")
        else:
            if not ctx.author.guild_permissions.administrator:
                ctx.command.reset_cooldown(ctx)
                return await ctx.send("Sneaky.")

        async with self.bot.session.get(START_LINK) as response:
            if response.status == 200:
                self.embed.description = "Status Code 200! Server startup sequence triggered."
                self.embed.color = discord.Color.green()
                self.embed.timestamp = datetime.datetime.now(tz=BOT_TZ)
                await ctx.send(embed=self.embed)
            self.running = True
            self.init_time = time.time()

    @commands.cooldown(1, 600, commands.BucketType.guild)
    @commands.command(name="stop-server", aliases=["stopserver"])
    async def stop_server(self, ctx, override: str=False):
        if override != "--override":
            if not self.running:
                ctx.command.reset_cooldown(ctx)
                return await ctx.send("Server is not running right now.")
            cur_time = time.time()
            diff = (cur_time - self.init_time) // 60
            if diff < 6:     # applies a 6 minute cooldown on shutdown command since start-up
                ctx.command.reset_cooldown(ctx)
                return await ctx.send(f"You're trying to shut the server down too quick. Time since start-up sequence ~{diff} mins")
        else:
            if not ctx.author.guild_permissions.administrator:
                ctx.command.reset_cooldown(ctx)
                link = self.bot.stupid_collection.find_one({'key':'no'})['output']
                return await ctx.send(link)

        async with self.bot.session.get(STOP_LINK) as response:
            if response.status == 200:
                cur_time = time.time()
                diff = (cur_time - self.init_time) // 60
                self.embed.description = f"Status Code 200. Server shutdown sequence triggered.\nServer uptime: {diff} minutes."
                self.embed.color = discord.Color.red()
                self.embed.timestamp = datetime.datetime.now(tz=BOT_TZ)
                await ctx.send(embed=self.embed)
            self.running = False
            self.init_time = time.time()
            
    @commands.command(name="uptime")
    async def uptime(self, ctx):
        diff = (time.time() - self.init_time) // 60
        return await ctx.send(f"Uptime: {diff} minutes") 

    @commands.command(name="server-variable-override")
    @commands.has_guild_permissions(administrator=True)
    async def server_variable_override(self, ctx, var, value):
        if var.lower() == "running":
            self.running = eval(value)
        elif var.lower() == "init_time":
            self.init_time = eval(value)
        return await ctx.send("Variables updated.")

def setup(bot):
    bot.add_cog(Minecraft(bot))
