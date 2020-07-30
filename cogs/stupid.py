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

rart = {
    "ayaz": "Sadia Ayaz from waste management"
}
class stupid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener() 
    async def on_message(self, message):
        if message.content.lower() == "damn":
            await message.add_reaction("🇩")
            await message.add_reaction("🅰️")
            await message.add_reaction("🇲")
            await message.add_reaction("🇳")
        elif message.content.lower() == "bruh":
            await message.add_reaction("🅱️")
            await message.add_reaction("🇷")
            await message.add_reaction("🇺")
            await message.add_reaction("🇭") 

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

    @commands.command(name="weird", aliases=["w"])
    async def weird(self, ctx, *, message):
        out = ''
        curr_func = "lower"
        for i in message:
            if curr_func == "lower":
                out += i.lower()
                curr_func = "upper"
            else:
                out += i.upper()
                curr_func = "lower"
        #await ctx.message.delete()
        await ctx.message.channel.send(out)

    @commands.group(pass_context=True)
    async def wat(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("bruh that isn't a thing.")

    @wat.command(name="add")
    async def add_to_wat(self, ctx, key, *, output):
        rart[key] = output
        await ctx.send("Added")

    @wat.command(name="remove")
    @commands.has_any_role(['Bot Dev'])
    async def remove_from_wat(self, ctx, key):
        try:
            rart.pop(key)
            await ctx.send(f"Removed {key}")
        except KeyError:
            await ctx.send(f"{key} doesn't exist")

    @wat.command(name="use")
    async def use(self, ctx, key):
        try:
            await ctx.send(rart[key])
        except KeyError:
            await ctx.send(f"{key} doesn't exist")

    @wat.command(name="list")
    async def list_(self, ctx):
        for i in rart.keys():
            await ctx.send(i)

    

def setup(bot):
    bot.add_cog(stupid(bot))