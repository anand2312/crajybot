import discord
from discord import guild
from discord.ext import commands, tasks
from discord.ext.commands.core import command
from pymongo import MongoClient
from aiohttp import ClientSession
from typing import Optional
import random
import datetime
from KEY import *       #rapidapi key


#API requests headers and URLs
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

ddg_url = "https://duckduckgo-duckduckgo-zero-click-info.p.rapidapi.com/"

ddg_headers =  {
    'x-rapidapi-host': "duckduckgo-duckduckgo-zero-click-info.p.rapidapi.com",
    'x-rapidapi-key': KEY
    }

#list of responses for .commit
commit_die = [
    "Go commit not alive",
"Go commit aliven't",
"Go commit uninstall life",
"Go commit discontinue life",
"Go commit short-circuit life",
"Go commit not feeling so good",
"Go commit blood not flow",
"Go commit death-pacito",
"Go commit sewer side",
"Go commit oxygen not reach lungs",
"Go commit heart not pumping blood",
"Go commit cease the means of carbon dioxide production",
"Go commit neck rope",
"Go commit wrist knife",
"Go commit jugular scissor",
"Go commit plug fork",
"Go commit swallow lit firework",
"Go commit celebrity's career after saying n-word",
"Go commit train track picnic",
"Go commit exhaust pipe succ",
"Go commit shove head in oven",
"Go commit skydive no parachute",
"Go commit 3 shots of cyanide",
"Go commit approach lion during safari",
"Go commit cliff jump",
"Go commit skinny dip in flood",
"Go commit gay in Iran",
"Go commit break into gun owner's home",
"Go commit XXXTentacion leave motorbike store, Go commit 30 days no eat",
"Go commit hold breath underwater for 10 minutes",
"Go commit bite dust",
"Go commit Logan Paul's reputation after suicide forest vlog",
"Go commit jump overboard on ferry",
'Go commit choir in "This is America" music video',
"Go commit motorway chicken",
"Go commit bully weird kid in American school Go commit dog in Sputnik rocket",
"Go commit bucket kick",
"Go commit fetus in liberal's womb",
"Go commit neck dislocate",
"Go commit Niagara Falls jump",
"Go commit Robbie Rotten cannonball hit",
"Go commit stare at enderman",
"Go commit swim in lava",
"Go commit oof IRL",
"Go commit Ukraine's population in 1930s",
"Go commit liver after 10 shots of vodka"
]

#MongoDB initialization
client = MongoClient("mongodb://localhost:27017/")
db = client["bot-data"]
stupid_collection = db["stupid"]
notes_collection = db["notes"]
bday_collection = db["bday"]

#aiohttp initialization for API requests
session = ClientSession()
#webhook initialization for sending .wat in #another-chat, #botspam
anotherchat_webhook = discord.Webhook.partial(740080790385459292, "8E-xPQqRcIJlVIp-_phep34DGW9T95Us9bgY1XQpFCMQRAO7-1NIj9La6HFSXMzQwNoy", adapter=discord.AsyncWebhookAdapter(session))
botspam_webhook = discord.Webhook.partial(740086899925975051, "URRNUuEI9NWxq_PYot0LAPfpw4jgvmBaffx5s26CL_ajNT7sJ075rjAuww2F90rRHcqt", adapter=discord.AsyncWebhookAdapter(session))


class stupid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.birthday_loop.start()
    @commands.command(name="fancy", aliases=["f"])
    async def fancy(self, ctx, *, message):
        querystring = {"text":message}
        async with ctx.channel.typing():
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
        async with ctx.channel.typing():
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

    @wat.command(name="add", aliases=["-a"])
    async def add_to_wat(self, ctx, key, *, output):
        stupid_collection.insert_one({"key":key, "output":output})
        await ctx.send("Added")

    @wat.command(name="remove", aliases=["-r"])
    @commands.has_any_role('admin','Bot Dev')
    async def remove_from_wat(self, ctx, key):
        try:
            stupid_collection.delete_one({"key":key})
            await ctx.message.channel.send(f"Removed {key}")
        except:
            await ctx.message.channel.send(f"{key} doesn't exist")

    @wat.command(name="edit-output", aliases=["edit-out"])
    async def edit_wat_output(self, ctx, key, *, output):
        try:
            stupid_collection.update_one({'key':key},{"$set":{"output":output}})
            await ctx.message.channel.send("Updated output.")
        except:
            await ctx.message.channel.send("Key doesn't exist")

    @wat.command(name="edit-key", aliases=["edit-name"])
    async def edit_wat_key(self, ctx, key, new_key):
        try:
            stupid_collection.update_one({'key':key},{"$set":{"key":new_key}})
            await ctx.message.channel.send("Updated name.")
        except:
            await ctx.message.channel.send("Key doesn't exist")    

    @wat.command(name="use", aliases=["-u"])
    async def use(self, ctx, key):
        data = stupid_collection.find_one({"key":key})["output"]
        if data is not None:
            if ctx.message.channel.name == "another-chat":
                await anotherchat_webhook.send(data, username=ctx.message.author.nick, avatar_url=ctx.message.author.avatar_url)
            elif ctx.message.channel.name == "botspam":
                await botspam_webhook.send(data, username=ctx.message.author.nick, avatar_url=ctx.message.author.avatar_url)
            else:
                await ctx.send(data)
        else:
            ctx.send("Not found.")

    @wat.command(name="list", aliases=["-l"])
    async def list_(self, ctx):
        out = ""
        for i in stupid_collection.find():
            out += i["key"] + "\n"
        await ctx.send(out)

    @wat.command(name="search", aliases=["-s"])
    async def wat_search(self, ctx, key):
        check = 0
        embed = discord.Embed(title="Search Results", color=discord.Color.blurple())
        for i in stupid_collection.find():
            if key.lower() in i["key"].lower():
                embed.add_field(name=i['key'], value=i['output'], inline=False)
                check += 1
        if check == 0:
            embed.add_field(name="No search results found", value=" ")
        await ctx.send(embed=embed)

    @commands.command(name="emojify", aliases=['e'])
    async def emojify(self, ctx, *, message):
        emojis = {'a':'🇦', 'b': '🇧', 'c':'🇨', 'd':'🇩', 'e':'🇪', 'f': '🇫', 'g': '🇬', 'h':'🇭', 'i': '🇮', 'j':'🇯', 'k':'🇰', 'l':'🇱', 'm':'🇲', 'n':'🇳', 'o':'🇴', 'p':'🇵', 'q':'🇶', 'r':'🇷', 's':'🇸', 't':'🇹', 'u':'🇺', 'v':'🇻', 'w':'🇼', 'x':'🇽', 'y':'🇾', 'z':'🇿'}
        out = ""
        for letter in message.lower():
            if letter.isalpha():
                out += f"{emojis[letter]} "
            else:
                out += letter
        await ctx.send(out)
    @wat.command(name="react")
    async def react(self, ctx, id_:discord.Message, *emojis):
        for i in emojis:
            await id_.add_reaction(i)
        await ctx.message.delete()

    @commands.command(name="owo", aliases=["uwu"])
    async def owo(self, ctx, *, text):
        out = ""
        for i in text:
            case = "upper" if i.isupper() else "lower"
            if i.lower() in ["l","r"]: out += "w" if case=="lower" else "W"
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

    @commands.group(name="commit", invoked_without_command=True)
    async def commit(self, ctx):
        await ctx.send(random.choice(commit_die))

    @commit.command(name="add", aliases=["-a"])
    async def commit_add(self, ctx, *,output):
        commit_die.append(output)
        await ctx.send("Added.")
    
    @commands.command(name="search") #under work
    async def ddg_search(self, ctx, *, query):
        querystring = {"no_redirect":"1","no_html":"1","callback":"process_duckduckgo","skip_disambig":"1","q":query,"format":"xml"}
        async with session.get(ddg_url, headers=ddg_headers, params=querystring) as response:
            return_text = await response.text()
            print(return_text)
        '''embed = discord.Embed(name="Search Results", color=discord.Color.dark_blue(), url=return_text["AbstractURL"])
        embed.add_field(name=return_text["Heading"], description=return_text["AbstractText"])
        embed.set_footer(text="Results from DuckDuckGo", icon_url=return_text["image"])
        await ctx.send(embed=embed)'''

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
        for person in bday_collection.find():
            person_obj = discord.utils.get(ctx.guild.members, name=person['user'].split('#')[0])
            response.add_field(name=person_obj.nick, value=person['date'].strftime('%d %B %Y'), inline=False)
        await ctx.send(embed=response)
    
    @tasks.loop(hours=24)
    async def birthday_loop(self):
        data = bday_collection.find()
        for person in data:
            if person['date'].strftime("%d-%B") == datetime.datetime.now().strftime('%d-%B'):
                person_obj = discord.utils.get(guild.members, name=person['user'].split("#")[0])
                await wishchannel.send(f"It's {person_obj.mention}'s birthday today! @everyone")
    
    @birthday_loop.before_loop
    async def birthdayloop_before(self):
        global guild
        global wishchannel
        await self.bot.wait_until_ready()
        guild = self.bot.get_guild(298871492924669954)
        wishchannel = guild.get_channel(392576275761332226)

def setup(bot):
    bot.add_cog(stupid(bot))