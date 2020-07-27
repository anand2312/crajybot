import discord 
from discord.ext import commands
import random
import asyncio
from pymongo import MongoClient
#do whatever imports you need; I've just done a few which I could think of

client = MongoClient("mongodb://localhost:27017/")
db = client["bot-data"]

economy_collection = db["econ_data"]
rpg_collection = db["rpg_data"]
store_collection = db["store_data"]

channels_available = ["bot-test","botspam-v2","botspam"]

class Moderator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="change-money",aliases=["c-money","cm"])                  #gives admins, mods the permission to change money to their own bank (for now)
    @commands.has_any_role("Bot Dev","Moderators","admin")                      #this allows multiple roles to have access to one command
    async def change_money(self,ctx,action:str,baltype:str,user:discord.Member,amt:int):
        user_data = economy_collection.find_one({'user':str(user)})
        if amt >= 0:
            action = action.lower()
            if action == "add":
                user_data[baltype] += amt
                response = discord.Embed(title = str(ctx.message.author.name), description = f"Added {amt} to {user}\'s {baltype}!" ,colour=discord.Colour.green())
                    
            elif action == "remove":
                user_data[baltype] -= amt
                response = discord.Embed(title = str(ctx.message.author.name), description = f"Removed {amt} from {user}\'s {baltype}!" ,colour=discord.Colour.red())

            elif action == "set":
                user_data[baltype] = amt
                response = discord.Embed(title = str(ctx.message.author.name), description = f"Set {amt} to {user}\'s {baltype}!" ,colour=discord.Colour.orange()) 

            economy_collection.update_one({'user':str(user)}, {"$set":user_data})
            if ctx.message.channel.name in channels_available: await ctx.message.channel.send(content=None,embed=response)
    
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

    @commands.command(name = "change-inventory",aliases=["c-inv"])
    @commands.has_any_role("Moderators","admin","Bot Dev")
    async def change_inventory(self,ctx,action:str,item:str,user:discord.Member,amt:int):
        user_data = economy_collection.find_one({'user':str(user)})
        action, item = action.lower(), item.lower()
        if action == "add":
            for i in user_data["inv"]:
                if item in i.keys():
                    i[item] += amt
                    response = discord.Embed(title = str(ctx.message.author.name), description = f"Added {amt} {item}(s) to {user}\'s inventory!",colour=discord.Colour.green())
                
        elif action == "remove":
            for i in user_data["inv"]:
                if item in i.keys():
                    i[item] -= amt
                    response = discord.Embed(title = str(ctx.message.author.name), description = f"Removed {amt} {item}(s) from {user}\'s inventory!",colour=discord.Colour.red())

        elif action == "set":
            for i in user_data["inv"]:
                if item in i.keys():
                    i[item] = amt
                    response = discord.Embed(title = str(ctx.message.author.name), description = f"Set {amt} {item}(s) to {user}\'s inventory!",colour=discord.Colour.orange())
        economy_collection.update_one({'user':str(user)},{"$set":user_data})
        if ctx.message.channel.name in channels_available: await ctx.message.channel.send(content = None, embed = response)

    
def setup(bot):
    bot.add_cog(Moderator(bot))