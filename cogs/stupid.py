import discord
from discord.ext import commands
import requests

fancy_url = "https://ajith-fancy-text-v1.p.rapidapi.com/text"

fancy_headers = {
    'x-rapidapi-host': "ajith-Fancy-text-v1.p.rapidapi.com",
    'x-rapidapi-key': "b93010ab3bmsh7c9b21f8a1e6182p17c090jsn3ff13f0b6d1d"
}

love_url = "https://love-calculator.p.rapidapi.com/getPercentage"

love_headers = {
    'x-rapidapi-host': "love-calculator.p.rapidapi.com",
    'x-rapidapi-key': "b93010ab3bmsh7c9b21f8a1e6182p17c090jsn3ff13f0b6d1d"
    }
class stupid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="fancy", aliases=["f"])
    async def fancy(self, ctx, *, message):
        querystring = {"text":message}
        response = requests.request("GET", fancy_url, headers=fancy_headers, params=querystring)
        await ctx.message.channel.send(response.json()["fancytext"].split(",")[0])

    @commands.command(name="love-calc", aliases=["lc","love","lovecalc"])
    async def love_calc(self, ctx, sname:str, fname=None):
        if fname is None:
            fname = str(ctx.message.author)
            querystring = {"fname":str(ctx.message.author),"sname":sname}
        else:
            querystring = {"fname":fname,"sname":sname}
        response = requests.request("GET", love_url, headers=love_headers, params=querystring)
        percent = response.json()["percentage"]
        result = response.json()["result"]
        if int(percent) >= 50:
            embed=discord.Embed(title="Love Calculator", colour=discord.Color.green())
            embed.set_author(name=fname)
            embed.add_field(name="That poor person", value=sname, inline=False)
            embed.add_field(name="Percent", value=percent, inline=True)
            embed.add_field(name="Result", value=result, inline=False)
        else:
            embed=discord.Embed(title="Love Calculator", colour=discord.Color.red())
            embed.set_author(name=fname)
            embed.add_field(name="That poor person", value=sname, inline=False)
            embed.add_field(name="Percent", value=percent, inline=True)
            embed.add_field(name="Result", value=result, inline=False)          
        sent_message = await ctx.message.channel.send(content=None, embed=embed)
        await sent_message.add_reaction("✅")
        await sent_message.add_reaction("❌")



def setup(bot):
    bot.add_cog(stupid(bot))