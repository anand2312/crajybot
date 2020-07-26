import discord 
from discord.ext import commands

class Battle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()