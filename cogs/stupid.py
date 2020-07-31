import discord
from discord.ext import commands
import requests
from pymongo import MongoClient
from itertools import count
#from KEY import KEY

fancy_url = "https://ajith-fancy-text-v1.p.rapidapi.com/text"

fancy_headers = {
    'x-rapidapi-host': "ajith-Fancy-text-v1.p.rapidapi.com",
    'x-rapidapi-key': KEY
}

love_url = "https://love-calculator.p.rapidapi.com/getPercentage"

love_headers = {
    'x-rapidapi-host': "love-calculator.p.rapidapi.com",
    'x-rapidapi-key': KEY
    }

client = MongoClient("mongodb://localhost:27017/")
db = client["bot-data"]

stupid_collection = db["stupid"]

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
        stupid_collection.insert_one({"key":key, "output":output})
        await ctx.send("Added")

    @wat.command(name="remove")
    @commands.has_any_role('admin','Bot Dev')
    async def remove_from_wat(self, ctx, key):
        try:
            stupid_collection.delete_one({"key":key})
            await ctx.send(f"Removed {key}")
        except:
            await ctx.send(f"{key} doesn't exist")

    @wat.command(name="use")
    async def use(self, ctx, key):
        try:
            await ctx.send(stupid_collection.find_one({"key":key})["output"])
        except:
            await ctx.send(f"{key} doesn't exist")

    @wat.command(name="list")
    async def list_(self, ctx):
        out = ""
        for i in stupid_collection.find():
            out += i["key"] + "\n"
        await ctx.send(out)
    

def setup(bot):
    bot.add_cog(stupid(bot))