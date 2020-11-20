import discord
from discord.ext import commands

from secret.TOKEN import START_LINK, STOP_LINK

class Minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.running = False

    #@commands.has_permissions(administrator=True)
    @commands.cooldown(1, 600, commands.BucketType.guild)
    @commands.command(name="start-server", aliases=["startserver"])
    async def start_server(self, ctx):
        if self.running:
            return await ctx.send("Server already running! IP: 35.241.144.6")
        
        async with self.bot.session.get(START_LINK) as response:
            if response.status == 200:
                await ctx.send("Server startup sequence triggered.")
            self.running = True

    #@commands.has_permissions(administrator=True)
    @commands.cooldown(1, 600, commands.BucketType.guild)
    @commands.command(name="stop-server", aliases=["stopserver"])
    async def stop_server(self, ctx):
        if not self.running:
            return await ctx.send("Server is not running right now.")

        async with self.bot.session.get(STOP_LINK) as response:
            if response.status == 200:
                await ctx.send("Server shutdown sequence triggered.")
            self.running = False

def setup(bot):
    bot.add_cog(Minecraft(bot))
