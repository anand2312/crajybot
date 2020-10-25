import discord 
from discord.ext import commands

import requests

import random
import asyncio
import typing
import git

from pymongo import MongoClient

from secret.TOKEN import GIT_HELPER
#do whatever imports you need; I've just done a few which I could think of

client = MongoClient("mongodb://localhost:27017/")
db = client["bot-data"]

economy_collection = db["econ_data"]
store_collection = db["store_data"]
games_leaderboard = db["games"]
stupid_collection = db["stupid"]
notes_collection = db["notes"]
bday_collection = db["bday"]
pins_collection = db["pins"]

channels_available = ["bot-test","botspam-v2","botspam"]

class Moderator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.git_helper_webhook = discord.Webhook.partial(GIT_HELPER['id'], GIT_HELPER['token'], adapter=discord.AsyncWebhookAdapter(self.bot.session))
        
    @commands.group(name="change-money",aliases=["c-money","cm"])                  #gives admins, mods the permission to change money to their own bank (for now)
    @commands.has_any_role("Bot Dev","Moderators","admin")                    
    async def change_money(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid action.")

    @change_money.command(name="add")
    async def add_money(self, ctx, baltype: str, user: discord.Member, amt: int):
        economy_collection.update_one({'user': user.id},{"$inc": {baltype:amt}})
        response = discord.Embed(title=str(ctx.message.author.name), description=f"Added {amt} to {user}\'s {baltype}!" ,colour=discord.Colour.green())
        await ctx.send(embed=response) 

    @change_money.command(name="remove")
    async def remove_money(self, ctx, baltype: str, user: discord.Member, amt: int):
        economy_collection.update_one({'user': user.id}, {"$inc": {baltype:-amt}})
        response = discord.Embed(title=str(ctx.author.name), description=f"Removed {amt} from {user}\'s {baltype}!" ,colour=discord.Colour.red())
        await ctx.send(embed=response)

    @change_money.command(name="set")
    async def set_money(self, ctx, baltype: str, user: discord.Member, amt: int):
        economy_collection.update_one({'user': user.id}, {"$set": {baltype: amt}})
        response = discord.Embed(title = str(ctx.message.author.name), description = f"Set {amt} to {user}\'s {baltype}!" ,colour=discord.Colour.orange()) 
        await ctx.send(embed=response)
    
    @commands.command(name = "change-stock")
    @commands.has_any_role("Moderators","admin","Bot Dev")
    async def change_stock(self, ctx, item:str, n:int):
        store_collection.update_one({'name': item.lower().capitalize()}, {"$set": {'stock': n}})     
        response = discord.Embed(title = str(ctx.message.author.name), description=f"Updated stock of {item}")
        if ctx.message.channel.name in channels_available: await ctx.message.channel.send(embed=response)

    @commands.command(name = "remove-user")
    @commands.has_any_role("Moderators","admin","Bot Dev")
    async def remove_user(self, ctx, member:discord.Member):
        try:
            economy_collection.delete_one({'user': member.id})
            await member.send(f"haha popi you got deleted from the bot database")
        except:
            await ctx.send("User not found")

    @commands.group(name = "change-inventory", aliases=["c-inv"])
    @commands.has_any_role("Moderators","admin","Bot Dev")
    async def change_inventory(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid action.")

    @change_inventory.command(name="add")
    async def add_inv(self, ctx, item: str, user: discord.Member, amt: int):
        user_data = economy_collection.find_one({'user': user.id})
        item = item.lower()
        user_data["inv"][item] += amt
        economy_collection.update_one({'user': user.id},{"$set": user_data})
        response = discord.Embed(title=str(ctx.author.name), description=f"Added {amt} {item}(s) to {user}\'s inventory!",colour=discord.Colour.green())
        await ctx.message.channel.send(embed=response)

    @change_inventory.command(name="remove")
    async def remove_inv(self, ctx, item: str, user: discord.Member, amt: int):
        user_data = economy_collection.find_one({'user': user.id})
        item = item.lower()
        user_data["inv"][item] -= amt
        economy_collection.update_one({'user': user.id},{"$set": user_data})
        response = discord.Embed(title=str(ctx.message.author.name), description=f"Removed {amt} {item}(s) from {user}\'s inventory!",colour=discord.Colour.red())
        await ctx.message.channel.send(embed=response)

    @change_inventory.command(name="set")
    async def set_inv(self, ctx, item: str, user: discord.Member, amt: int):
        user_data = economy_collection.find_one({'user': user.id})
        item = item.lower()
        user_data["inv"][item] = amt
        economy_collection.update_one({'user': user.id},{"$set": user_data})
        response = discord.Embed(title=str(ctx.message.author.name), description=f"Set {amt} {item}(s) to {user}\'s inventory!",colour=discord.Colour.orange())
        await ctx.message.channel.send(content=None, embed=response)

    @commands.command(name="change-price")
    @commands.has_any_role("Moderators","admin","Bot Dev")
    async def change_price(self, ctx, item:str, price:int):
        store_collection.update_one({'name':item.lower().capitalize()}, {"$set": {"price": price}})
        await ctx.send("Price changed")

    @commands.command(name="query")
    @commands.has_any_role("admin")
    async def mongo_query(self, ctx, database, action, filter=None, update=None):
        pass

    @commands.command(name="clear-pin", aliases=["clearpins", "clear-pins"])
    @commands.has_guild_permissions(administrator=True)
    async def remove_pins(self, ctx, id_: typing.Union[int, str]):
        if isinstance(id_, int):
            x = pins_collection.delete_one({"_id":id_})
            if x.deleted_count > 0:
                return await ctx.send(f"Deleted pin with ID {id_}")
            else:
                return await ctx.send("No pin with that ID could be found")

        else:
            if id_.lower() == "all":
                def check(m):
                    return m.author==ctx.author and m.content.lower() in ['yes','y','no','n']
                await ctx.send("Are you sure you want to clear all pins?")
                reply = await self.bot.wait_for('message', check=check, timeout=10)
                if reply.content.lower() in ["yes", "y"]:
                    pins_collection.delete_many({})
                    return await ctx.send("Cleared all pins")
                else:
                    return await ctx.send("Terminated.")

    @commands.has_guild_permissions(administrator=True)
    @commands.command(name="pin")
    async def pin(self, ctx, id_: discord.Message, name_: str=None):
        old_data = pins_collection.find().sort("_id", -1).limit(1)
        try:
            last_pin = old_data[0]['_id']
        except IndexError:
            last_pin = 0
        document = dict(_id= last_pin+1,
            message_synopsis = id_.content[:30] + "...",
            message_jump_url = id_.jump_url,
            message_author = id_.author.name,
            date = datetime.date.today().strftime('%B %d, %Y'),
            name = name_)

        pins_collection.insert_one(document)

        await id_.add_reaction("📌")
        reply_embed = discord.Embed(title=f"Pinned!", description=f"_{document['message_synopsis'][:10]+'...'}_\n with ID {last_pin+1}", color=discord.Color.green())
        reply_embed.set_thumbnail(url= r"https://media.discordapp.net/attachments/612638234782072882/758190572526764052/emoji.png?width=58&height=58")
        reply_embed.set_footer(text=f"Pinned by {ctx.author.name}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=reply_embed)

    @commands.has_any_role("Bot Dev")
    @commands.command(name="server-update", aliases=["git-pull", "gitpull", "serverupdate"])
    async def server_update(self, ctx):
        try:
            out = git.cmd.Git().pull(r"https://github.com/AbsoluteMadlad12/CrajyBot-private", "master")
        except Exception as e:
            await ctx.message.add_reaction("❌")
            return await ctx.send(embed=discord.Embed(title="Unexpected error", description=str(e), color=discord.Color.red()))

        await ctx.message.add_reaction("✅")
        if out != "Already up to date.":
            embed = discord.Embed(title="Server Update: **Complete**", color=discord.Color.green())
            embed.description = f"```fix\n{out}\n```"
            embed.set_footer(text=f"Requested by {ctx.author.name}")
        else:
            embed = discord.Embed(title="Server Update: _Already up to date_", color=discord.Color.orange())
            embed.set_footer(text=f"Requested by {ctx.author.name}")

        await self.git_helper_webhook.send(username="Crajy Helper", embed=embed)
    
def setup(bot):
    bot.add_cog(Moderator(bot))