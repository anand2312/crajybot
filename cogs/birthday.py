import discord
from discord.ext import commands
import datetime

"""Moved birthday related commands here"""

class Birthday(commands.Cog):
    def __init__(self,  bot):
        self.bot = bot

    @commands.group(name="bday", aliases=["birthday"], invoke_without_command=True)
    async def bday(self, ctx, person: discord.Member=None):
        if person is None:
            person = ctx.message.author
        date = bday_collection.find_one({"user":str(person)})
        await ctx.send(embed=discord.Embed(title=f"{person.nick}'s birthday", description=f"{date['date'].strftime('%d %B %Y')}", color=discord.Color.blurple()))
        

    @bday.command(name="add", aliases=["-a"])
    async def bday_add(self, ctx, person: discord.Member=None):
        if person is None:
            person = ctx.message.author
        
        await ctx.send(f"Send {person.nick}'s birthday, in DD-MM-YYYY format")
        def check(m):
            return m.author == ctx.message.author and len(m.content.split("-")) == 3 and m.guild is not None

        reply = await self.bot.wait_for('message', check=check, timeout=30)
        date_vals = list(map(int, reply.content.split("-")))

        bday_collection.update_one({'user':str(person)}, {'$set':{'date':datetime.datetime(date_vals[2], date_vals[1], date_vals[0])}}, upsert=True)

        await ctx.send(f"Added {person.nick}'s birthday to the database. He shall be wished 😔")

    @bday.command(name="all")
    async def bday_all(self, ctx):
        response = discord.Embed(title="Everyone's birthdays", color=discord.Color.blurple())
        for person in bday_collection.find().sort('date', ASCENDING):
            person_obj = discord.utils.get(ctx.guild.members, name=person['user'].split('#')[0])
            response.add_field(name=person_obj.nick, value=person['date'].strftime('%d %B %Y'), inline=False)
        await ctx.send(embed=response)

    def find_horoscope_sign(self, date: datetime.datetime) -> str:
        str_date = date.strftime('%d %B').split()
        pass

def setup(bot):
    bot.add_cog(Birthday(bot))