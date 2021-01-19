"""Some functions to remember and wish your server members."""
import discord
from discord.ext import commands
import datetime

from internal import enumerations as enums
from utils import embed as em

class Birthday(commands.Cog):
    def __init__(self,  bot):
        self.bot = bot

    @commands.group(name="bday", 
                    aliases=["birthday"],
                    help="Retrieve a birthday date. Could be your own if no user is specified, or a specified user.", 
                    invoke_without_command=True)
    async def bday(self, ctx, person: discord.Member = None):
        date = await self.bot.db_pool.fetchval("SELECT bday FROM user_details WHERE user_id=$1", person.id)
        embed = em.CrajyEmbed(title=f"{person.nick}'s birthday", description=date.strftime('%d %B %Y'), embed_type=enums.EmbedType.INFO)
        embed.set_thumbnail(em.EmbedResource.BDAY.value)
        embed.quick_set_author(person)
        
        today = datetime.datetime.today()
        this_year_date = datetime.date(year=today.year, month=date.month, day=date.day)
        remaining = this_year_date - today

        embed.set_footer(text=f"Their birthday is in {remaining}")

        await ctx.maybe_reply(embed=embed)
        

    @bday.command(name="add",
                  aliases=["-a"],
                  help="Add a birthday date. Could be your own if no user is specified, or a specified user.")
    async def bday_add(self, ctx, person: discord.Member = None):
        if person is None:
            person = ctx.author
        
        ask_embed = em.CrajyEmbed(title=f"Setting Birthday for {person.nick}", embed_type=enums.EmbedType.INFO)
        ask_embed.description = f"Enter the date in DD-MM-YYYY format"
        ask_embed.set_thumbnail(url=em.EmbedResource.BDAY.value)
        ask_embed.quick_set_author(person)

        ask_message = await ctx.maybe_reply(embed=ask_embed)

        def check(m):
            return m.author == ctx.author and len(m.content.split("-")) == 3 and m.guild is not None

        reply = await self.bot.wait_for('message', check=check, timeout=30)
        date_vals =[int(i) for i in reply.content.split("-")]
        kwargs = ("day", "month", "year")

        await self.bot.db_pool.execute("UPDATE user_details SET bday $1 WHERE user_id=$2", datetime.date(**zip(kwargs, date_vals)), person.id)
        
        out = em.CrajyEmbed(title=f"Birthday Set!", embed_type=enums.EmbedType.SUCCESS)
        out.description = f"{person.nick}'s birthday is saved. They shall be wished."
        out.set_thumbnail(url=em.EmbedResource.BDAY.value)
        out.quick_set_author(person)

        return await ask_message.edit(embed=out)

    @bday.command(name="all",
                  help="Get a list of all birthdays saved.")
    async def bday_all(self, ctx):
        response = em.CrajyEmbed(title="Everyone's birthdays", embed_type=enums.EmbedType.INFO)
        response.set_thumbnail(url=em.EmbedResource.BDAY.value)

        all_data = await self.bot.db_pool.fetch("SELECT user_id, bday FROM user_details")
        
        for person in all_data:    
            person_obj = discord.utils.get(ctx.guild.members, id=person['user_id'])
            if person_obj is None:
                continue
            response.add_field(name=person_obj.nick, value=person['bday'].strftime('%d %B %Y'), inline=False)
        await ctx.maybe_reply(embed=response)

    def find_horoscope_sign(self, date: datetime.datetime) -> str:
        """WIP for future functionality."""
        str_date = date.strftime('%d %B').split()
        pass

def setup(bot):
    bot.add_cog(Birthday(bot))