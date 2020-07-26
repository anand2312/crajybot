import discord
from discord.ext import commands
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["bot-data"]

economy_collection = db["econ_data"]
rpg_collection = db["rpg_data"]
store_collection = db["store_data"]

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        await bot.get_channel(703141348131471440).send("its popi time!!")
        await bot.change_presence(activity = discord.Game(name = "with thug_sgt"))

    @commands.command(name = "withdraw", aliases = ["with"])
    async def withdraw(ctx,amount):
        try:
            amount = int(amount)
            if economy_collection.find_one({'user':str(ctx.message.author)})['bank'] >= amount:
                economy_collection.find_one_and_update({'user':str(ctx.message.author)},{"$inc":{'bank':(amount*(-1)), 'cash':amount}})
                response = discord.Embed(title = str(ctx.message.author), description = f"Withdrew {amount}", colour = discord.Color.green())
                await ctx.message.channel.send(content = None, embed = response)
            else:
                await ctx.message.channel.send("You do not have that much balance")
        except ValueError:
            if amount.lower() == "all":
                user_data = economy_collection.find_one({'user':str(ctx.message.author)})
                economy_collection.find_one_and_update({'user':str(ctx.message.author)},{"$set":{'bank':0, 'cash':user_data['cash']+user_data['bal']}})
                response = discord.Embed(title = str(ctx.message.author), description = f"""Withdrew {i["bank"]}""", colour = discord.Color.green())
                await ctx.message.channel.send(content = None, embed = response)

def setup(bot):
    bot.add_cog(Economy(bot))
