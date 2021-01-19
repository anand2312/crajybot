"""Some fun commands."""
import discord
from discord.ext import commands, tasks

from typing import Optional, Union
import random

from contextlib import suppress
import more_itertools as mitertools

from secret.constants import GUILD_ID, ROLE_NAME
from secret.KEY import *  
from secret.TOKEN import *  

from utils import embed as em
from internal import enumerations as enums

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

class Stupid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.pin_cache = set()
        self.pin_vote_threshold = 4
        # a loop that changes the name of a role, based on names saved in the database. Names are added with the `role-name` command

        self.bot.task_loops['role_name'] = self.role_name_loop  
        self.bot.task_loops['qotd_cache'] = self.qotd_cache_loop

        try:
            self.anotherchat_webhook = discord.Webhook.partial(ANOTHERCHAT_HOOK['id'], ANOTHERCHAT_HOOK['token'], adapter=discord.AsyncWebhookAdapter(self.bot.session))
            self.botspam_webhook = discord.Webhook.partial(BOTSPAM_HOOK['id'], BOTSPAM_HOOK['token'], adapter=discord.AsyncWebhookAdapter(self.bot.session))
        except:
            pass

        self.cached_qotd = None

    @commands.Cog.listener()
    async def on_message(self, message):
        # REWRITE THIS.
        if message.author.bot: return
        currencies = {"usd", "omr", "inr", "eur"}
        message_string = message.content.lower().replace("euro", "eur")
        message_string = message_string.replace("rial", "omr")
        message_string = message_string.replace("rupees", "inr")
        message_string = message_string.replace("rs", "inr")

        converted = []
        splitted = message_string.split()

        for index, word in enumerate(splitted):
            if word in currencies:
                init_cur = word
                number = int(splitted[index-1])
                break
        
        url1 = f"https://free.currconv.com/api/v7/convert?apiKey={CURRENCY_KEY}&q={init_cur}_OMR,{init_cur}_INR"
        url2 = f"https://free.currconv.com/api/v7/convert?apiKey={CURRENCY_KEY}&q={init_cur}_USD,{init_cur}_EUR"
        async with self.bot.session.get(url1) as resp1, self.bot.session.get(url2) as resp2:
            data1 = await resp1.json()
            data2 = await resp2.json()
            rates = {}
            for key, value in data1["results"].items():
                if value["val"] != 1:
                    rates[key] = value["val"]
            for key, value in data2["results"].items():
                if value["val"] != 1:
                    rates[key] = value["val"]

        for key, value in rates.items():
            res_string = f"{key[4:]} {value * number}"
            converted.append(res_string)
        joined = "\n".join(converted)
        out = f"{number} {init_cur} is:\n{joined}"
        return await message.reply(out)
                
    async def on_reaction_add(self, reaction, user):
        if str(reaction) == "📌" and user != self.bot.user:
            if reaction.message in self.pin_cache:
                if reaction.count == self.pin_vote_threshold:
                    mod = self.bot.get_cog("Moderator")
                    ctx = await self.bot.get_context(reaction.message)
                    setattr(ctx, "author", self.bot.user)
                    self.pin_cache.remove(reaction.message)
                    await reaction.message.clear_reactions()
                    return await mod.pin(ctx, id_=reaction.message)
            else:
                self.pin_cache.add(reaction.message)
        
    @commands.command(name="fancy", aliases=["f"])
    async def fancy(self, ctx, *, message):
        querystring = {"text":message}
        async with ctx.channel.typing():
            async with self.bot.session.get(fancy_url, headers=fancy_headers, params=querystring) as response:
                return_text = await response.json()
                return_text = return_text["fancytext"].split(",")[0]
            await ctx.maybe_reply(return_text)

    @commands.command(name="love-calc", aliases=["lc","love","lovecalc"])
    async def love_calc(self, ctx, sname : str, fname=None):
        # why are we using an API here; just randomize.
        if fname is None:
            fname = str(ctx.author)
            querystring = {"fname":str(ctx.message.author),"sname":sname}
        else:
            querystring = {"fname":str(fname),"sname":str(sname)}
        async with ctx.channel.typing():
            async with self.bot.session.get(love_url, headers=love_headers, params=querystring) as response:
                percent = await response.json()
                percent = percent["percentage"]
                result = await response.json()
                result = result["result"]
            if int(percent) >= 50:
                embed = em.CrajyEmbed(title="Love Calculator", embed_type=enums.EmbedType.SUCCESS)
                embed.quick_set_author(ctx.author)
                embed.set_thumbnail(url=em.EmbedResource.LOVE_CALC.value)
                embed.add_field(name="That poor person", value=sname, inline=False)
                embed.add_field(name="Percent", value=percent, inline=True)
                embed.add_field(name="Result", value=result, inline=False)
            else:
                embed=discord.Embed(title="Love Calculator", embed_type=enums.EmbedType.FAIL)
                embed.quick_set_author(ctx.author)
                embed.set_thumbnail(url=em.EmbedResource.LOVE_CALC.value)
                embed.add_field(name="That poor person", value=sname, inline=False)
                embed.add_field(name="Percent", value=percent, inline=True)
                embed.add_field(name="Result", value=result, inline=False)          
            sent_message = await ctx.maybe_reply(embed=embed)
            await ctx.check_mark(sent_message)

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
        await ctx.maybe_reply(out)
    
    @commands.command(name="emojify", aliases=['e'])
    async def emojify(self, ctx, *, message):
        emojis = {'a':'🇦', 'b': '🇧', 'c':'🇨', 'd':'🇩', 'e':'🇪', 'f': '🇫', 'g': '🇬', 'h':'🇭', 'i': '🇮', 'j':'🇯', 'k':'🇰', 'l':'🇱', 'm':'🇲', 'n':'🇳', 'o':'🇴', 'p':'🇵', 'q':'🇶', 'r':'🇷', 's':'🇸', 't':'🇹', 'u':'🇺', 'v':'🇻', 'w':'🇼', 'x':'🇽', 'y':'🇾', 'z':'🇿'}
        out = ""
        for letter in message.lower():
            if letter.isalpha():
                out += f"{emojis[letter]} "
            else:
                out += letter
        await ctx.maybe_reply(out)

    @commands.command(name="owo", aliases=["uwu"])
    async def owo(self, ctx, *, text):
        out = ""
        for i in text:
            case = "upper" if i.isupper() else "lower"
            if i.lower() in ["l","r"]: out += "w" if case=="lower" else "W"
            else: out+=i

        await ctx.maybe_reply(out)
        
    @commands.command(name="pins", help="Display the messages pinned in the bot database. Useful if your channel has already reached the 50 pin limit.")
    async def pins(self, ctx): 
        data = await self.bot.db_pool.fetch("SELECT pin_id, synopsis, jump_url, author, date FROM pins")

        embeds = []

        for chunk in mitertools.chunked(data, 6):
            embed = em.CrajyEmbed(title=f"{ctx.guild.name} Pins!", embed_type=enums.EmbedType.INFO)
            embed.set_thumbnail(url=em.EmbedResource.TAG.value)
            embed.quick_set_author(ctx.author)

            for pin in chunk:
                author = ctx.guild.get_member(pin['author'])
                if author is None:
                    continue    # in case user has left the server, ignore their pin
                embed.add_field(name=f"{pin['synopsis']}",
                                value=f"[_~{author.display_name}_, on {pin['date']}]({pin['jump_url']})\nPin ID:{pin['pin_id']}", 
                                inline=False)

            embeds.append(embed)

        pages = em.quick_embed_paginate(embeds)
        await pages.start(ctx)

    @commands.command(name="fetch-pin", aliases=["fetchpin"], help="Return a pin based on the ID provided. WIP.")
    async def fetch_pin(self, ctx, identifier: Union[str, int]):

        if identifier.isalpha():
            data = await self.bot.db_pool.execute("SELECT pin_id, synopsis, jump_url, date FROM pins WHERE name=$1", identifier)
        elif identifier.isdigit():
            data = await self.bot.db_pool.execute("SELECT pin_id, synopsis, jump_url, date FROM pins WHERE pin_id=$1", identifier)

        embed = em.CrajyEmbed(title=f"Pin **{data['_id']}**", url=data["jump_url"], embed_type=enums.EmbedType.INFO)
        embed.description = f"**{data['synopsis']}**\n  _by {data['author']} on {data['date']}_"
        embed.set_thumbnail(url=em.EmbedResource.TAG)
        embed.set_footer(text=f"Requested by {ctx.author.nick}. Click on the embed title to go to the message.", icon_url=ctx.author.avatar_url)
        return await ctx.maybe_reply(embed=embed)

    @commands.has_guild_permissions(administrator=True)
    @commands.command(name="change-vote-threshold", help="Change the minimum votes required to pin a message.")
    async def change_vote_threshold(self, ctx, arg: int):
        self.pin_vote_threshold = arg
        await ctx.check_mark()
        
    @commands.group(name="role-name", aliases=["rolename", "rolenames"], invoke_without_command=True)
    async def role_name(self, ctx, *, name: str):

        await self.bot.db_pool.execute("INSERT INTO role_names(role_name, author) VALUES ($1, $2)", name, ctx.author.id)

        embed = em.CrajyEmbed(title="Added!", description=f"`{name}` was added to the database. It will be picked randomly.", embed_type=enums.EmbedType.SUCCESS, url=r"https://www.youtube.com/watch?v=DLzxrzFCyOs")
        embed.quick_set_author(ctx.author)
        embed.set_thumbnail(url=em.EmbedResource.PIN.value)

        return await ctx.send(embed=embed)

    @role_name.command(name="list", aliases=["all"])
    async def role_name_list(self, ctx):
        data = await self.bot.db_pool.fetch("SELECT role_name, author FROM role_names")
        embed = em.CrajyEmbed(title="Role names", embed_type=enums.EmbedType.BOT)
        embed.set_thumbnail(url=em.EmbedResource.PIN.value)
        out = []
        for i in data:
            author = ctx.get_member(i['author'])
            line = f"• **{i['role_name']}**, _by {author.display_name}_"
            out.append(line)
        embed.description = "\n".join(out)
        return await ctx.send(embed=embed)

    @role_name.command(name="remove", aliases=["delete"])
    @commands.has_guild_permissions(administrator=True)
    async def role_name_remove(self, ctx, *names: str):      # can pass multiple role names to bulk delete. each arg must be wrapped in quotes.
        await self.bot.db_pool.execute("DELETE FROM role_names WHERE LOWER(role_name) = ANY($1)", names)

        embed = em.CrajyEmbed(title="Deleting Role Names", embed_type=enums.EmbedType.BOT)
        listed_names = '\n'.join(f'• {i}' for i in names)
        embed.description = f"Deleted:\n ```{listed_names}```"
        embed.set_thumbnail(url=em.EmbedType.TRASHCAN.value)
        embed.quick_set_author(self.bot.user)
        embed.set_footer(text="Note: Names are deleted if they existed in the database in the first place.")

        await ctx.reply(embed=embed)

    @commands.command(name="quote", aliases=["qotd"], help="Displays a random quote.")
    async def qotd(self, ctx):
        await ctx.reply(self.cached_qotd, mention_author=False)

    @commands.command(name="change-presence", aliases=["changepresence", "changestatus", "change-status"], help="Change the bot's status.")
    @commands.cooldown(1, 600, type=commands.BucketType.guild)
    async def change_presence(self, ctx, activity: str, *, status: str):
        if activity.lower() not in ["playing", "watching", "listening", "streaming"]:
            raise ValueError('Status has to be one of `"playing", "watching", "listening", "streaming"`')
        
        if len(status) > 30:
            raise ValueError(f"Inputted status ({len(status)}) longer than 30 characters.")

        discord_activity = discord.Activity(name=status)

        if activity.lower() == "playing":
            discord_activity.type = discord.ActivityType.playing
        elif activity.lower() == "listening":
            discord_activity.type = discord.ActivityType.listening
        elif activity.lower() == "watching":
            discord_activity.type = discord.ActivityType.watching
        elif activity.lower() == "streaming":
            discord_activity = discord.Streaming(name=activity)
            
        await ctx.check_mark()
        return await self.bot.change_presence(status=discord.Status.online, activity=discord_activity)

    @tasks.loop(hours=1)
    async def qotd_cache_loop(self):
        # DOES THIS STILL WORK?
        """The quotes.rest API has a very strict limit on number of requests that are given for free, so
        instead of making requests everytime the command is called, this loop does the request once an hour and 
        caches it for further use."""
        async with self.bot.session.get(r"http://quotes.rest/qod.json") as response:
            data = await response.json()
        self.cached_qotd = f"{data['contents']['quotes'][0]['quote']}\n~{data['contents']['quotes'][0]['author']}"
        return

    @qotd_cache_loop.before_loop
    async def before_qotd_cache(self):
        await self.bot.wait_until_ready()
        
    @tasks.loop(hours=12)
    async def role_name_loop(self):
        guild = self.bot.get_guild(GUILD_ID)
        role = guild.get_role(ROLE_NAME)
        existing = await self.bot.db_pool.fetch("SELECT role_name FROM role_names")
        new_name_data = random.choice(data)
        await role.edit(name=new_name_data['role_name'])

    @role_name_loop.before_loop
    async def rolename_before(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(Stupid(bot))
