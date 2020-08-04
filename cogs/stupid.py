import discord
from discord import webhook
from discord.ext import commands
from discord.ext.commands.core import command
from pymongo import MongoClient
from aiohttp import ClientSession
from KEY import *

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
notes_collection = db["notes"]

session = ClientSession()
anotherchat_webhook = discord.Webhook.partial(740080790385459292, "8E-xPQqRcIJlVIp-_phep34DGW9T95Us9bgY1XQpFCMQRAO7-1NIj9La6HFSXMzQwNoy", adapter=discord.AsyncWebhookAdapter(session))
botspam_webhook = discord.Webhook.partial(740086899925975051, "URRNUuEI9NWxq_PYot0LAPfpw4jgvmBaffx5s26CL_ajNT7sJ075rjAuww2F90rRHcqt", adapter=discord.AsyncWebhookAdapter(session))


class stupid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="fancy", aliases=["f"])
    async def fancy(self, ctx, *, message):
        querystring = {"text":message}
        async with session.get(fancy_url, headers=fancy_headers, params=querystring) as response:
            return_text = await response.json()
            return_text = return_text["fancytext"].split(",")[0]
            await ctx.send(return_text)
    @commands.command(name="love-calc", aliases=["lc","love","lovecalc"])
    async def love_calc(self, ctx, sname:str, fname=None):
        if fname is None:
            fname = str(ctx.message.author)
            querystring = {"fname":str(ctx.message.author),"sname":sname}
        else:
            querystring = {"fname":fname,"sname":sname}
        async with session.get(love_url, headers = love_headers, params=querystring) as response:
            percent = await response.json()
            percent = percent["percentage"]
            result = await response.json()
            result = result["result"]
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

    @wat.command(name="edit-output", aliases=["edit-out"])
    async def edit_wat(self, ctx, key, *, output):
        try:
            stupid_collection.update_one({'key':key},{"$set":{"output":output}})
            await ctx.send("Updated.")
        except:
            await ctx.send("Key doesn't exist")

    @wat.command(name="edit-key", aliases=["edit-name"])
    async def edit_wat(self, ctx, key, new_key):
        try:
            stupid_collection.update_one({'key':key},{"$set":{"key":new_key}})
            await ctx.send("Updated.")
        except:
            await ctx.send("Key doesn't exist")    

    @wat.command(name="use")
    async def use(self, ctx, key):
        '''try:
            await ctx.send(stupid_collection.find_one({"key":key})["output"])
            #await ctx.message.delete()
        except:
            await ctx.send(f"{key} doesn't exist")'''
        data = stupid_collection.find_one({"key":key})["output"]

        if ctx.message.channel.name == "another-chat":
            await anotherchat_webhook.send(data, username=ctx.message.author.nick, avatar_url=ctx.message.author.avatar_url)
        elif ctx.message.channel.name == "botspam":
            await botspam_webhook.send(data, username=ctx.message.author.nick, avatar_url=ctx.message.author.avatar_url)
        else:
            await ctx.send(data)

    @wat.command(name="list")
    async def list_(self, ctx):
        out = ""
        for i in stupid_collection.find():
            out += i["key"] + "\n"
        await ctx.send(out)

    '''@wat.command(name="react")
    async def react(self, ctx, id_:discord.Message, *emojis):
        for i in emojis:
            await id_.add_reaction(i)
        #await ctx.message.delete()'''

    @commands.command(name="owo", aliases=["uwu"])
    async def owo(self, ctx, *, text):
        out = ""
        for i in text:
            if i.lower() in ["l","r"]: out+="w"
            else: out+=i

        await ctx.send(out)

    @commands.group(pass_context=True)
    async def notes(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("bruh that isn't a thing.")

    @notes.command(name="create", aliases=["-c"])
    async def notes_create(self, ctx, *, content):
        current = notes_collection.find_one({"user":str(ctx.message.author)})
        if current is None: current = "\n"
        else: current = current["notes"]
        notes_collection.update_one({"user":str(ctx.message.author)},{"$set":{"notes":current + content + "\n"}}, upsert=True)
        await ctx.send("Added to notes. Do ``.notes return`` to get everything stored.")

    @notes.command(name="return", aliases=["-r"])
    async def notes_return(self, ctx):
        try:
            await ctx.message.author.send(notes_collection.find_one({"user":str(ctx.message.author)})["notes"])
            await ctx.message.author.send("Use ``.notes pop`` to delete existing notes")
        except TypeError:
            await ctx.send("No notes.")

    @notes.command(name="pop", aliases=["-p"])
    async def notes_pop(self, ctx):
        notes_collection.delete_one({"user":str(ctx.message.author)})
        await ctx.send("Notes cleared.")
def setup(bot):
    bot.add_cog(stupid(bot))