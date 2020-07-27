import discord 
from discord.ext import commands
import random
import asyncio
from pymongo import MongoClient
#do whatever imports you need; I've just done a few which I could think of

client = MongoClient("mongodb://localhost:27017/")
db = client["bot-data"]

economy_collection = db["econ_data"]
store_collection = db["store_data"]

channels_available = ["bot-test","botspam-v2","botspam"]

class Betting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "roulette")
    async def roulette(self, ctx, amount:int, bet:str):
        user_dict = economy_collection.find_one({'user':str(ctx.message.author)})

        if amount <= user_dict['cash'] and user_dict['cash'] > 0:

            roulette_table = {
                "red" : [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36],
                "black" : [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 31, 33, 35],
                "1st" : [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34],
                "2nd" : [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35],
                "3rd" : [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36],
                "odd" : None,
                "even" : None,
                "1-12": None,
                "13-24": None,
                "25-36":None,
                "1-18":None,
                "19-36":None

            }
            if bet in roulette_table.keys():
                win_number = random.randint(0,36)
                user_dict['cash'] -= amount
                economy_collection.update_one({'user':str(ctx.message.author)},{"$set":user_dict})
                response1 = discord.Embed(title = str(ctx.message.author), description = f"You've placed a bet on {bet}.")
                response1.set_footer(text = f"Please wait 10 seconds")
                await ctx.message.channel.send(content = None, embed = response1)
                
                user_win = False
                if bet == "red" or bet == "black":          #colour
                    if win_number in roulette_table[bet]:
                        user_win = True
                        multiplier = 2
                    else:
                        user_win = False

                elif bet in ["1-12", "13-24", "25-36"]:         #dozens
                    if bet == "1-12":
                        if win_number in range(1,13):
                            user_win = True
                            multiplier = 3
                        else:
                            user_win = False
                    elif bet == "13-24":
                        if win_number in range(13,25):
                            user_win = True
                            multiplier = 3
                        else:
                            user_win = False
                    elif bet == "25-36":
                        if win_number in range(25,37):
                            user_win = True
                            multiplier = 3
                        else:
                            user_win = False

                elif bet in ["even","odd"]:    #odd/even
                    if bet == "even":
                        if win_number % 2 == 0:
                            user_win = True
                            multiplier = 2
                    elif bet == "odd":
                        if win_number % 2 != 0:
                            user_win = True
                            multiplier = 2

                elif bet in ["1-18","19-36"]:       #halves
                    if bet == "1-18":
                        if win_number in range(1,19):
                            user_win = True
                            multiplier = 2
                    else:
                        if win_number in range(19,37):
                            user_win = True
                            multiplier = 2

                elif bet in ["1st", "2nd", "3rd"]:               #columns
                    if win_number in roulette_table[bet]:
                        user_win = True
                        multiplier = 3
                    
                
            elif int(bet) in range(0,37):
                win_number = random.randint(0,36)
                user_win = False
                user_dict['cash'] -= amount
                economy_collection.update_one({'user':str(ctx.message.author)},{"$set":user_dict})

                response1 = discord.Embed(title = str(ctx.message.author), description = f"You've placed a bet on {bet}.")
                response1.set_footer(text = f"Please wait 10 seconds")
                await ctx.message.channel.send(content = None, embed = response1)

                if win_number == int(bet):
                    user_win = True
                    multiplier = 36
            
            else:
                await ctx.message.channel.send(f'Invalid bet.')
                return

            await asyncio.sleep(10)
            if user_win is True:
                response2 = discord.Embed(title = f"Roulette Results {str(ctx.message.author)}", description = f"You won {multiplier * amount}!", colour = discord.Color.green())
                economy_collection.update_one({'user':str(ctx.message.author)},{"$inc":{'cash':multiplier * amount}})
                if ctx.message.channel.name in channels_available: 
                    await ctx.message.channel.send(f"The ball fell on {win_number}")
                    await ctx.message.channel.send(content = None, embed = response2)
            else:
                response2 = discord.Embed(title = f"Roulette Results {str(ctx.message.author)}", description = f"You lost {amount} {self.bot.get_emoji(703648812669075456)}", colour = discord.Color.red())
                if ctx.message.channel.name in channels_available: 
                    await ctx.message.channel.send(f"The ball fell on {win_number}")
                    await ctx.message.channel.send(content = None, embed = response2)
        else:
            await ctx.message.channel.send(f"nigga what you trying? you don't have that much moni")

    
    @commands.command(name = "reverse-russian-roulette", aliases = ["rrr"])
    async def russian_roulette(self, ctx, amount:int):
        response = discord.Embed(title = "Russian Roulette", description = f"{str(ctx.message.author)} started a round of russian roulette for {amount}. Click on the reaction below in the next 15 seconds to join.")
        if ctx.message.channel.name in channels_available: rr_message_init = await ctx.message.channel.send(content = None, embed = response)
        await rr_message_init.add_reaction(self.bot.get_emoji(703648812669075456))
        await asyncio.sleep(15)
        rr_message = await ctx.message.channel.fetch_message(rr_message_init.id)
        
        users_list = await rr_message.reactions[0].users().flatten()
        users_list.pop(0)

        rrr_cursor = economy_collection.find({'user':{"$in":users_list}})
        rrr_data_full = []
        for i in rrr_cursor: rrr_data_full.append(i)

        for user_dict in rrr_data_full:
            if user_dict["cash"] >= amount:
                user_dict["cash"] -= amount
            elif user_dict["cash"] < amount:
                users_list.remove(user_dict['user'])   #UNSURE IF THIS WORKS, CHECK IF IT BREAKS
                await ctx.message.channel.send(f"{user_dict['user']} does not have enough balance")

        winner = random.choice(users_list)
        
        for i in users_list:
            if i != winner:
                response = discord.Embed(title = str(i), description = f"Got shot.", colour = discord.Color.red())
                await ctx.message.channel.send(content = None, embed = response)
                await asyncio.sleep(2)
            else:
                response = discord.Embed(title = str(i), description = "Survived!!", colour = discord.Color.green())
                await ctx.message.channel.send(content = None, embed = response)
                for user_dict in rrr_data_full:
                    if user_dict["user"] == str(winner):
                        user_dict["cash"] += (len(users_list) * amount)
        economy_collection.update_many({'user':{"$in":users_list}},{"$set":rrr_data_full})

    @commands.command(name = "cock-fight", aliases = ["cf","cockfight"])
    async def cockfight(self,ctx,amount:int):
        user_data = economy_collection.find_one({'user':str(ctx.message.author)})
        win = random.choice([True,False,False,False])
        if amount > 0 and amount <= user_data["cash"]:
            if user_data["inv"][1]["chicken"] > 0:
                user_data["inv"][1]["chicken"] -= 1
                if win is True:
                    user_data["cash"] += amount
                    response = discord.Embed(title = str(ctx.message.author), description = f"Your little cock one the fight, making you {amount} richer!", colour = discord.Color.green())
                else:
                    user_data["cash"] -= amount
                    response = discord.Embed(title = str(ctx.message.author), description = f"Your cock is weak. It lost the fight.", colour = discord.Color.red())
            else:
                await ctx.message.channel.send("You don't have enough cocks. Buy one!")
        else:
            await ctx.message.channel.send("Invalid bet.")
        economy_collection.update_one({'user':str(ctx.message.author)},{"$set":user_data})
        if ctx.message.channel.name in channels_available: await ctx.message.channel.send(content = None, embed = response)

def setup(bot):
    bot.add_cog(Betting(bot))