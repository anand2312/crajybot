"""Some commands to store user notes."""
import discord
from discord.ext import commands

class Notes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def notes(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("bruh that isn't a thing.")

    @notes.command(name="create", aliases=["-c"])
    async def notes_create(self, ctx, *, content):
        current = self.bot.notes_collection.find_one({"user": ctx.author.id})
        if current is None: current = "\n"
        else: current = current["notes"]
        self.bot.notes_collection.update_one({"user":ctx.author.id},{"$set":{"notes":current + content + "\n"}}, upsert=True)
        await ctx.send("Added to notes. Do ``.notes return`` to get everything stored.")

    @notes.command(name="return", aliases=["-r"])
    async def notes_return(self, ctx):
        try:
            await ctx.author.send(self.bot.notes_collection.find_one({"user":ctx.author.id})["notes"])
            await ctx.author.send("Use ``.notes pop`` to delete existing notes")
        except TypeError:
            await ctx.send("No notes.")

    @notes.command(name="pop", aliases=["-p"])
    async def notes_pop(self, ctx):
        self.bot.notes_collection.delete_one({"user":ctx.author.id})
        await ctx.send("Notes cleared.")

def setup(bot):
    bot.add_cog(Notes(bot))