import discord
from discord.ext import commands

from secret.TOKEN import START_LINK, STOP_LINK

class Minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(administrator=True)
    @commands.command(name="start-server", aliases=["startserver"])
    async def start_server(self, ctx):
        async with self.bot.session.get(START_LINK) as response:
            if response.status == 200:
                await ctx.send("Server startup sequence triggered.")

    @commands.has_permissions(administrator=True)
    @commands.command(name="stop-server", aliases=["stopserver"])
    async def stop_server(self, ctx):
        async with self.bot.session.get(STOP_LINK) as response:
            if response.status == 200:
                await ctx.send("Server shutdown sequence triggered.")

def setup(bot):
    bot.add_cog(Minecraft(bot))