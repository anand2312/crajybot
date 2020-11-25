"""Some functions to remember and wish your server members."""
import discord
from discord.ext import commands
import datetime
from pymongo import ASCENDING

class Birthday(commands.Cog):
    def __init__(self,  bot):
        self.bot = bot

    @commands.group(name="bday", 
                    aliases=["birthday"],
                    help="Retrieve a birthday date. Could be your own if no user is specified, or a specified user.", 
                    invoke_without_command=True)
    async def bday(self, ctx, person: discord.Member=None):
        if person is None:
            person = ctx.author
        date = self.bot.bday_collection.find_one({"user": int(person.id)})
        await ctx.send(embed=discord.Embed(title=f"{person.nick}'s birthday", description=f"{date['date'].strftime('%d %B %Y')}", color=discord.Color.blurple()))
        

    @bday.command(name="add",
                  aliases=["-a"],
                  help="Add a birthday date. Could be your own if no user is specified, or a specified user.")
    async def bday_add(self, ctx, person: discord.Member=None):
        if person is None:
            person = ctx.author
        
        await ctx.send(f"Send {person.nick}'s birthday, in DD-MM-YYYY format")
        def check(m):
            return m.author == ctx.author and len(m.content.split("-")) == 3 and m.guild is not None

        reply = await self.bot.wait_for('message', check=check, timeout=30)
        date_vals = list(map(int, reply.content.split("-")))

        self.bot.bday_collection.update_one({'user': int(person.id)}, {'$set': {'date':datetime.datetime(date_vals[2], date_vals[1], date_vals[0])}}, upsert=True)

        await ctx.send(f"Added {person.nick}'s birthday to the database. He shall be wished 😔")

    @bday.command(name="all",
                  help="Get a list of all birthdays saved.")
    async def bday_all(self, ctx):
        response = discord.Embed(title="Everyone's birthdays", color=discord.Color.blurple())
        for person in self.bot.bday_collection.find().sort('date', ASCENDING):
            person_obj = discord.utils.get(ctx.guild.members, id=person['user'])
            if person_obj is None:
                continue
            response.add_field(name=person_obj.nick, value=person['date'].strftime('%d %B %Y'), inline=False)
        await ctx.send(embed=response)

    def find_horoscope_sign(self, date: datetime.datetime) -> str:
        """WIP for future functionality."""
        str_date = date.strftime('%d %B').split()
        pass

def setup(bot):
    bot.add_cog(Birthday(bot))