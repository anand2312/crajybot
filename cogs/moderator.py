import discord 
from discord.ext import commands

import requests

import random
import asyncio
import typing
import git

from pymongo import MongoClient

from secret.TOKEN import GIT_HELPER

channels_available = ["bot-test","botspam-v2","botspam"]

class Moderator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.git_helper_webhook = discord.Webhook.partial(GIT_HELPER['id'], GIT_HELPER['token'], adapter=discord.AsyncWebhookAdapter(self.bot.session))
    
    async def cog_check(self, ctx):
        return ctx.author.guild_permissions.administrator

    @commands.group(name="change-money",aliases=["c-money","cm"])               
    async def change_money(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid action.")

    @change_money.command(name="add")
    async def add_money(self, ctx, baltype: str, user: discord.Member, amt: int):
        self.bot.economy_collection.update_one({'user': user.id},{"$inc": {baltype:amt}})
        response = discord.Embed(title=str(ctx.message.author.name), description=f"Added {amt} to {user}\'s {baltype}!" ,colour=discord.Colour.green())
        await ctx.send(embed=response) 

    @change_money.command(name="remove")
    async def remove_money(self, ctx, baltype: str, user: discord.Member, amt: int):
        self.bot.economy_collection.update_one({'user': user.id}, {"$inc": {baltype:-amt}})
        response = discord.Embed(title=str(ctx.author.name), description=f"Removed {amt} from {user}\'s {baltype}!" ,colour=discord.Colour.red())
        await ctx.send(embed=response)

    @change_money.command(name="set")
    async def set_money(self, ctx, baltype: str, user: discord.Member, amt: int):
        self.bot.economy_collection.update_one({'user': user.id}, {"$set": {baltype: amt}})
        response = discord.Embed(title = str(ctx.message.author.name), description = f"Set {amt} to {user}\'s {baltype}!" ,colour=discord.Colour.orange()) 
        await ctx.send(embed=response)

    @commands.command(name="remove-user")
    async def remove_user(self, ctx, member: discord.Member):
        try:
            self.bot.economy_collection.delete_one({'user': member.id})
            await member.send(f"haha popi you got deleted from the bot database")
        except:
            await ctx.send("User not found")

    @commands.group(name="change-inventory", aliases=["c-inv"])
    async def change_inventory(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid action.")

    @change_inventory.command(name="add")
    async def add_inv(self, ctx, item: str, user: discord.Member, amt: int):
        user_data = self.bot.economy_collection.find_one({'user': user.id})
        item = item.lower()
        user_data["inv"][item] += amt
        self.bot.economy_collection.update_one({'user': user.id},{"$set": user_data})
        response = discord.Embed(title=str(ctx.author.name), description=f"Added {amt} {item}(s) to {user}\'s inventory!",colour=discord.Colour.green())
        await ctx.send(embed=response)

    @change_inventory.command(name="remove")
    async def remove_inv(self, ctx, item: str, user: discord.Member, amt: int):
        user_data = self.bot.economy_collection.find_one({'user': user.id})
        item = item.lower()
        user_data["inv"][item] -= amt
        self.bot.economy_collection.update_one({'user': user.id},{"$set": user_data})
        response = discord.Embed(title=str(ctx.message.author.name), description=f"Removed {amt} {item}(s) from {user}\'s inventory!",colour=discord.Colour.red())
        await ctx.send(embed=response)

    @change_inventory.command(name="set")
    async def set_inv(self, ctx, item: str, user: discord.Member, amt: int):
        user_data = self.bot.economy_collection.find_one({'user': user.id})
        item = item.lower()
        user_data["inv"][item] = amt
        self.bot.economy_collection.update_one({'user': user.id},{"$set": user_data})
        response = discord.Embed(title=str(ctx.message.author.name), description=f"Set {amt} {item}(s) to {user}\'s inventory!",colour=discord.Colour.orange())
        await ctx.send(content=None, embed=response)

    @commands.group(name="edit-item", aliases=["edititem"])
    async def edit_item(self, ctx):
        if ctx.invoked_subcommand is None: return await ctx.send("Invalid action")

    @edit_item.command(name="price")
    async def edit_item_price(self, ctx, item: str, price: int):
        self.bot.store_collection.update_one({'name':item.lower().capitalize()}, {"$set": {"price": price}})
        await ctx.send("Price changed")

    @edit_item.command(name="change-stock")
    async def change_stock(self, ctx, item: str, n: int):
        self.bot.store_collection.update_one({'name': item.lower().capitalize()}, {"$set": {'stock': n}})     
        response = discord.Embed(title = str(ctx.message.author.name), description=f"Updated stock of {item}")
        return await ctx.send(embed=response)

    @commands.command(name="clear-pin", aliases=["clearpins", "clear-pins"])
    async def remove_pins(self, ctx, id_: typing.Union[int, str]):
        if isinstance(id_, int):
            x = self.bot.pins_collection.delete_one({"_id":id_})
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
                    self.bot.pins_collection.delete_many({})
                    return await ctx.send("Cleared all pins")
                else:
                    return await ctx.send("Terminated.")

    @commands.command(name="pin")
    async def pin(self, ctx, id_: discord.Message, name_: str=None):
        old_data = self.bot.pins_collection.find().sort("_id", -1).limit(1)
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

        self.bot.pins_collection.insert_one(document)

        await id_.add_reaction("📌")
        reply_embed = discord.Embed(title=f"Pinned!", description=f"_{document['message_synopsis'][:10]+'...'}_\n with ID {last_pin+1}", color=discord.Color.green())
        reply_embed.set_thumbnail(url= r"https://media.discordapp.net/attachments/612638234782072882/758190572526764052/emoji.png?width=58&height=58")
        reply_embed.set_footer(text=f"Pinned by {ctx.author.name}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=reply_embed)

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

    @commands.command(name="bruh-id")
    async def bruh_id(self, ctx):
        for i in self.bot.notes_collection.find():
            user = discord.utils.get(ctx.guild.members, name=i['user'].split("#")[0])
            self.bot.notes_collection.update_one({"user": i['user']}, {"$set": {'user': user.id}})
            await ctx.send(f"Updated record for {user.nick}")
    
def setup(bot):
    bot.add_cog(Moderator(bot))