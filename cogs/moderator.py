import discord 
from discord.ext import commands
import random
import asyncio
import typing
from pymongo import MongoClient
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

    @commands.group(name="change-money",aliases=["c-money","cm"], pass_context=True)                  #gives admins, mods the permission to change money to their own bank (for now)
    @commands.has_any_role("Bot Dev","Moderators","admin")                      #this allows multiple roles to have access to one command
    async def change_money(self,ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid action.")

    @change_money.command(name="add")
    async def add_money(self, ctx, baltype:str, user:discord.Member, amt:int):
        economy_collection.update_one({'user':str(user)},{"$inc":{baltype:amt}})
        response = discord.Embed(title = str(ctx.message.author.name), description = f"Added {amt} to {user}\'s {baltype}!" ,colour=discord.Colour.green())
        await ctx.message.channel.send(content=None, embed=response) 

    @change_money.command(name="remove")
    async def remove_money(self, ctx, baltype:str, user:discord.Member, amt:int):
        economy_collection.update_one({'user':str(user)},{"$inc":{baltype:-amt}})
        response = discord.Embed(title = str(ctx.message.author.name), description = f"Removed {amt} from {user}\'s {baltype}!" ,colour=discord.Colour.red())
        await ctx.message.channel.send(content=None, embed=response)

    @change_money.command(name="set")
    async def set_money(self, ctx, baltype:str, user:discord.Member, amt:int):
        economy_collection.update_one({'user':str(user)},{"$set":{baltype:amt}})
        response = discord.Embed(title = str(ctx.message.author.name), description = f"Set {amt} to {user}\'s {baltype}!" ,colour=discord.Colour.orange()) 
        await ctx.message.channel.send(content=None, embed=response)
    
    @commands.command(name = "change-stock")
    @commands.has_any_role("Moderators","admin","Bot Dev")
    async def change_stock(self, ctx, item:str, n:int):
        store_collection.update_one({'name':item.lower().capitalize()}, {"$set":{'stock':n}})     
        response = discord.Embed(title = str(ctx.message.author.name), description = f"Updated stock of {item}")
        if ctx.message.channel.name in channels_available: await ctx.message.channel.send(content = None, embed = response)

    @commands.command(name = "remove-user")
    @commands.has_any_role("Moderators","admin","Bot Dev")
    async def remove_user(self, ctx, member:discord.Member):
        try:
            economy_collection.delete_one({'user':str(member)})
            await member.send(f"haha popi you got deleted from the bot database")
        except:
            await ctx.message.channnel.send("User not found")

    @commands.group(name = "change-inventory",aliases=["c-inv"], pass_context=True)
    @commands.has_any_role("Moderators","admin","Bot Dev")
    async def change_inventory(self,ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid action.")

    @change_inventory.command(name="add")
    async def add_inv(self, ctx, item:str, user:discord.Member, amt:int):
        user_data = economy_collection.find_one({'user':str(user)})
        item = item.lower()
        user_data["inv"][item] += amt
        economy_collection.update_one({'user':str(user)},{"$set":user_data})
        response = discord.Embed(title = str(ctx.message.author.name), description = f"Added {amt} {item}(s) to {user}\'s inventory!",colour=discord.Colour.green())
        await ctx.message.channel.send(content=None, embed=response)

    @change_inventory.command(name="remove")
    async def remove_inv(self, ctx, item:str, user:discord.Member, amt:int):
        user_data = economy_collection.find_one({'user':str(user)})
        item = item.lower()
        user_data["inv"][item] -= amt
        economy_collection.update_one({'user':str(user)},{"$set":user_data})
        response = discord.Embed(title = str(ctx.message.author.name), description = f"Removed {amt} {item}(s) from {user}\'s inventory!",colour=discord.Colour.red())
        await ctx.message.channel.send(content=None, embed=response)

    @change_inventory.command(name="set")
    async def set_inv(self, ctx, item:str, user:discord.Member, amt:int):
        user_data = economy_collection.find_one({'user':str(user)})
        item = item.lower()
        user_data["inv"][item] = amt
        economy_collection.update_one({'user':str(user)},{"$set":user_data})
        response = discord.Embed(title = str(ctx.message.author.name), description = f"Set {amt} {item}(s) to {user}\'s inventory!",colour=discord.Colour.orange())
        await ctx.message.channel.send(content=None, embed=response)

    @commands.command(name="change-price")
    @commands.has_any_role("Moderators","admin","Bot Dev")
    async def change_price(self, ctx, item:str, price:int):
        store_collection.update_one({'name':item.lower().capitalize()}, {"$set":{"price":price}})
        await ctx.send("Price changed")

    @commands.command(name="query")
    @commands.has_any_role("admin")
    async def mongo_query(self, ctx, database, action, filter=None, update=None):
        pass

    @commands.command(name="clear-pin", aliases=["clearpins", "clear-pins"])
    @commands.has_any_role("admin", "Moderators")
    async def remove_pins(self, ctx, id_: typing.Union[int, str]):
        if isinstance(id_, int):
            x = pins_collection.delete_one({"_id":id_})
            if x.deleted_count > 0:
                return await ctx.send(f"Deleted tag with ID {id_}")
            else:
                return await ctx.send("No tag with that ID could be found")

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
def setup(bot):
    bot.add_cog(Moderator(bot))