"""
Horoscopebot
insert further documentation here, insert documentation near new functions or variables you make as well.

"""
import os
import random
import discord 
from discord.ext import commands,tasks
import asyncio
import json
from random import choice

#bot token stuff; not to be messed with :linus_gun:
token_ = "NzA5NDA3MjY4NDg3MDM3MDE5.XuNH-A.sfVNk1d8Ky269KnpR4khtj6k6McY"
token = token_[:len(token_)-1]


#bot which controls everything; subclass of Client
bot = commands.Bot(command_prefix='$')

channels_available = ["bot-test","botspam-v2","botspam"] #Channels where the bot works
bot.remove_command('help') 
#Lets us implement our own help command instead of the built in one

@bot.event
async def on_ready(): #sends this message when bot starts working in #bot-tests
    await bot.get_channel(703141348131471440).send("its popi time!!")
    await bot.change_presence(activity = discord.Game(name = "with thug_sgt"))

@bot.event
async def on_member_join(member):
    with open("economy-data.json","r") as data:
        update_user_data = json.load(data)
    
    for i in update_user_data:
        if str(member) != i["user"]:
            check = False
            continue
        elif str(member) == i["user"]:
            check = True
            break

    if check is False:
        update_user_data.append({
                "user" : str(member),
                "cash" : 0,
                "bank" : 2500,
                "inv" : [
                    {"stock" : 0},
                    {"chicken" : 0},
                    {"heist tools" : 0}
                ],
                "debt" : 0,
                "zodiac_sign" : ""
            })
        with open("economy-data.json", "w") as data:
            json.dump(update_user_data,data)
        await member.send("You have been added to our bot database!")
    else:
        return

#ctx stands for context

#tryna test a function that matches member list and brings user data from economy json
def ReturnUserDict(inputName:discord.Member):           #function returns correct user dictionary from economy-data.json, AND the username (together in a tuple, unpack to use!)
    with open("economy-data.json","r") as data:
        user_data_list = json.load(data)
    for i in user_data_list:
        if i['user'] == str(inputName):
            return i, str(inputName)

@bot.command(name='popi')
async def popi(ctx):
    reply = random.choice(["poopi really do be poopie though",f"{ctx.message.author.mention} is a poopie?oh no......"]) #Choice chooses 1 object from the list
    response = discord.Embed(title='popi',description=reply)
    if ctx.message.channel.name in channels_available: await ctx.message.channel.send(content=None,embed=response)

@bot.command(name='help')
async def help(ctx):
    response = discord.Embed(title = "Help", description = "Click on the appropriate emoji within 10 seconds")
    response.add_field(name = "Economy Commands", value = "Click on the 🤑 emoji.", inline = False)
    response.add_field(name = "Battle Commands", value = "Click on the ⚔️ emoji", inline = False)
    response.add_field(name = "Moderator Commands", value = "Click on the 🔨 emoji", inline = False)
    message = await ctx.message.channel.send(content = None, embed = response)

    await message.add_reaction('🤑')
    await message.add_reaction('⚔️')
    await message.add_reaction('🔨')
    await asyncio.sleep(10)

    message = await ctx.message.channel.fetch_message(message.id)
    rxns = message.reactions
    for i in rxns:
        if i.count > 1:
            if i.emoji == '🤑':
                embed=discord.Embed(title="Economy Commands", description="List of Economy commands")
                embed.add_field(name="Income commands", value="work, slut, crime", inline=False)
                embed.add_field(name="$shop", value="Displays available items in shop.", inline=False)
                embed.add_field(name="$inv <user>", value="Displays selected user's inv, if not specified displays your inv", inline=False)
                embed.add_field(name="$buy <number> <item>", value="Buys item from shop.", inline=False)
                embed.add_field(name="$sell <number> <item>", value="Sells item back to shop.", inline=False)
                embed.add_field(name="$bal <user>", value="Displays your balance. Works similar to inv", inline=False)
                embed.add_field(name="$with <amount>", value="Withdraw amount from your bank", inline=False)
                embed.add_field(name="$dep <amount>", value="Deposit amount to bank", inline=False)
                embed.add_field(name="$givemoney <user> <amount>", value="Donate money to others.", inline=False)
                embed.add_field(name="$get-loan <amount>", value="Get a loan of specified amount", inline=False)
                embed.add_field(name="$repay-loan", value="Repay your loan (completely, not bit by bit)", inline=False)
                embed.add_field(name="$roulette <amount> <bet>", value="Roulette", inline=False)
                embed.add_field(name="$rrr <amount>", value="Starts a session of Reverse Russian Roulette", inline=False)
                embed.add_field(name="$cf <amount>", value="Cock fight.", inline=False)
                await message.edit(content = None, embed = embed)
            elif i.emoji == '⚔️':   
                embed = discord.Embed(title="Battle!", description="under development")
                await message.edit(content = None, embed = embed)
            elif i.emoji == '🔨':
                embed = discord.Embed(title="Moderator Commands", description = "List of moderator commands")
                embed.add_field(name="$change-money <action> <cash/bank> <user> <amount>", value = "Action can be remove/add/set.")
                embed.add_field(name="$c-inv <action> <amount> <item> <user>", value = "Same actions as $cm, but for inventory.")
                embed.add_field(name="$change-stock <item> <number>", value ="Used to change stock remaining of an item in shop.")
                await message.edit(content = None, embed = embed)
            break
     
#ECONOMY CODE; ADD SPACE ABOVE THIS FOR OTHER UNRELATED FUNCTIONS PLEASE :linus_gun:
@bot.command(name = "withdraw", aliases = ["with"])
async def withdraw(ctx,amount):
    try:
        amount = int(amount)
        with open("economy-data.json","r") as data:
            with_data = json.load(data)
            for i in with_data:
                if i["user"] == str(ctx.message.author):
                    if i["bank"] >= amount:
                        i["bank"] -= amount
                        i["cash"] += amount
                        with open("economy-data.json","w") as data:
                            json.dump(with_data,data)
                        response = discord.Embed(title = str(ctx.message.author), description = f"Withdrew {amount}", colour = discord.Color.green())
                        await ctx.message.channel.send(content = None, embed = response)
                    else:
                        await ctx.message.channel.send("You do not have that much balance")
    except ValueError:
        if amount.lower() == "all":
            with open("economy-data.json","r") as data:
                with_data = json.load(data)
            for i in with_data:
                if i["user"] == str(ctx.message.author):
                    i["cash"] += i["bank"]
                    response = discord.Embed(title = str(ctx.message.author), description = f"""Withdrew {i["bank"]}""", colour = discord.Color.green())
                    i["bank"] = 0
                    with open("economy-data.json","w") as data:
                        json.dump(with_data,data)
                    await ctx.message.channel.send(content = None, embed = response)

@bot.command(name = "deposit", aliases = ["dep"])
async def deposit(ctx,amount):
        try:
            amount = int(amount)
            with open("economy-data.json","r") as data:
                dep_data = json.load(data)
                for i in dep_data:
                    if i["user"] == str(ctx.message.author):
                        if i["cash"] >= amount:
                            i["bank"] += amount
                            i["cash"] -= amount
                            with open("economy-data.json","w") as data:
                                json.dump(dep_data,data)
                            response = discord.Embed(title = str(ctx.message.author), description = f"Deposited {amount}", colour = discord.Color.green())
                            await ctx.message.channel.send(content = None, embed = response)
                        else:
                            await ctx.message.channel.send("Not that much moni to deposit")
        except ValueError:
            if amount.lower() == "all":
                with open("economy-data.json","r") as data:
                    dep_data = json.load(data)
                for i in dep_data:
                    if i["user"] == str(ctx.message.author):
                        i["bank"] += i["cash"]
                        response = discord.Embed(title = str(ctx.message.author), description = f"""Deposited {i["cash"]}""", colour = discord.Color.green())
                        i["cash"] = 0
                        with open("economy-data.json","w") as data:
                            json.dump(dep_data,data)
                        await ctx.message.channel.send(content = None, embed = response)
@bot.command(name='bal')
async def balance(ctx,user:discord.Member):
    user_dict, username = ReturnUserDict(user)

    networth = (user_dict["cash"] + user_dict["bank"]) - user_dict["debt"]
    
    response = discord.Embed(title=username, description="Balance is:")
    response.add_field(name="Cash Balance : ",value=f"{user_dict['cash']}", inline = False)
    response.add_field(name="Bank balance : ",value=f"{user_dict['bank']}", inline = False)
    response.add_field(name="Debt : ",value=f"{user_dict['debt'] * (-1)}", inline = False)
    response.add_field(name="Net Worth : ",value=networth, inline = False)
                       #all this is for 1) in Bank, 2) Debt, 3) Total bal

    if ctx.message.channel.name in channels_available: await ctx.message.channel.send(content=None,embed=response)

@balance.error
async def bal_error(ctx,error):
    if isinstance(error , commands.errors.MissingRequiredArgument):
        with open("economy-data.json","r") as data:
            data_bal = json.load(data)
        
        for x in data_bal:
            if x["user"] == str(ctx.message.author):
                user_dict = x

        networth = (user_dict["cash"] + user_dict["bank"]) - user_dict["debt"]

        response = discord.Embed(title=str(ctx.message.author), description="Your balance is:")
        response.add_field(name="Cash balance : ",value=f"{user_dict['cash']}", inline = False)
        response.add_field(name="Bank balance : ",value=f"{user_dict['bank']}", inline = False)
        response.add_field(name="Debt : ",value=f"{user_dict['debt'] * (-1)}", inline = False)
        response.add_field(name="Net Worth : ",value=networth, inline = False)

        if ctx.message.channel.name in channels_available: await ctx.message.channel.send(content=None,embed=response)

@bot.command(name='work')
@commands.cooldown(1, 3600, commands.BucketType.user)            #remember to increase the cooldown to at least an hour!
async def work(ctx):
        with open("economy-data.json","r") as data:
            data_bal = json.load(data)
        for i in data_bal:
            if i["user"] == str(ctx.message.author):
                user_index = data_bal.index(i)
        

        rand_val = random.randint(35,150)
        data_bal[user_index]["cash"] += rand_val
        with open("economy-data.json", "w") as data:
            json.dump(data_bal,data)    #changing value in main json file as well

        response = discord.Embed(title=str(ctx.message.author),description=f"You earned {rand_val}",colour=discord.Colour.green())

    
        if ctx.message.channel.name in channels_available: await ctx.message.channel.send(content=None,embed=response)

@bot.command(name='slut')
@commands.cooldown(1, 3600, commands.BucketType.user)            #remember to increase the cooldown to at least an hour!
async def slut(ctx):
    with open("economy-data.json","r") as data:
        data_bal = json.load(data)
    for i in data_bal:
        if i["user"] == str(ctx.message.author):
            user_index = data_bal.index(i)

    winning_odds=[1,2,3,4,5,6]
    if random.randint(1,10) in winning_odds:
        rand_val = random.randint(60,200)
        data_bal[user_index]["cash"] += rand_val
        response = discord.Embed(title=str(ctx.message.author),description=f"You whored out and earned {rand_val}!",colour=discord.Colour.green())
    
    else:
        rand_val = random.randint(60,200)
        data_bal[user_index]["cash"] -= rand_val
        response = discord.Embed(title=str(ctx.message.author),description=f"You hooked up with a psychopath lost {rand_val}!",colour=discord.Colour.red())

    with open("economy-data.json","w") as data:
        json.dump(data_bal,data)

    if ctx.message.channel.name in channels_available: await ctx.message.channel.send(content=None,embed=response)

@bot.command(name="crime")
@commands.cooldown(1, 3600, commands.BucketType.user)            #remember to increase the cooldown to at least an hour!
async def crime(ctx):
    with open("economy-data.json","r") as data:
        data_bal = json.load(data)
    for i in data_bal:
        if i["user"] == str(ctx.message.author):
            user_index = data_bal.index(i)

    winning_odds=[1,2,3,4]
    if random.randint(1,10) in winning_odds:
        rand_val = random.randint(150,400)
        data_bal[user_index]["cash"] += rand_val
        response = discord.Embed(title=str(ctx.message.author),description=f"You successfuly commited crime and earned {rand_val}!",colour=discord.Colour.green())
    
    else:
        rand_val = random.randint(150,300)
        data_bal[user_index]["cash"] -= rand_val
        response = discord.Embed(title=str(ctx.message.author),description=f"You got caught and were fined {rand_val}!",colour=discord.Colour.red())

    with open("economy-data.json","w") as data:
        json.dump(data_bal,data)

    if ctx.message.channel.name in channels_available: await ctx.message.channel.send(content=None,embed=response)

@work.error
async def work_error(ctx,error):             #only says "CommandOnCooldown", not the time remaining
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.message.channel.send(commands.CommandOnCooldown.__name__)
                           
@slut.error
async def slut_error(ctx,error):             #only says "CommandOnCooldown", not the time remaining
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.message.channel.send(commands.CommandOnCooldown.__name__)

@crime.error
async def crime_error(ctx,error):             #only says "CommandOnCooldown", not the time remaining
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.message.channel.send(commands.CommandOnCooldown.__name__)

@bot.command(name = "leaderboard", aliases = ["top","lb"])
async def leaderboard(ctx):
    with open("economy-data.json","r") as data:
        leaderboard_data = json.load(data)

    for i in range(0,len(leaderboard_data)):
        for j in range(0,len(leaderboard_data) - 1 - i):
            if leaderboard_data[j]["bank"] + leaderboard_data[j]["cash"] > leaderboard_data[j + 1]["bank"] + leaderboard_data[j + 1]["cash"]:
                leaderboard_data[j],leaderboard_data[j+1] = leaderboard_data[j+1],leaderboard_data[j]

    leaderboard_data.reverse()

    response = discord.Embed(title = "Crajy Leaderboard", description = "")
    for i in leaderboard_data:
        response.add_field(name = f"{leaderboard_data.index(i)}. {i['user']}", value = f"Balance {i['bank'] + i['cash']}", inline = False)
    if ctx.message.channel.name in channels_available: await ctx.message.channel.send(content = None, embed = response)

@bot.command(name="get-loan", aliases = ["gl"])    #repayment made; finetuning required
async def loan(ctx,loan_val:int):
    
    with open("economy-data.json","r") as data:
        loan_data = json.load(data)
    for i in loan_data:
        if i["user"] == str(ctx.message.author):
            user_index = loan_data.index(i)
    if loan_val < loan_data[user_index]["bank"] * 2 and loan_data[user_index]["debt"] == 0:
        response = discord.Embed(title=str(ctx.message.author),description=f"You took a loan of {loan_val}!",colour=discord.Colour.red()) # red bc u did a dum dum

        loan_data[user_index]["debt"] = loan_data[user_index]["debt"] + (loan_val + int(loan_val * 0.05))
        loan_data[user_index]["bank"] += loan_val
        
        with open("economy-data.json","w") as data:
            json.dump(loan_data,data)
        if ctx.message.channel.name in channels_available: await ctx.message.channel.send(content=None,embed=response)

        await asyncio.sleep(64800)                                  #checks if debt has been repaid, if not sends reminder
        with open("economy-data.json","r") as data:
            loan_data = json.load(data)
        if loan_data[user_index]["debt"] != 0:                      
            await ctx.message.author.send("You're about to default on your loan")
        else:
            return
        
        await asyncio.sleep(21600)
        with open("economy-data.json","r") as data:
            loan_data = json.load(data)
        if loan_data[user_index]["debt"] != 0:
            loan_data[user_index]["debt"] = 0
            loan_data[user_index]["cash"] -= (loan_val + int(loan_val * 0.1))
            with open("economy-data.json","w") as data:
                json.dump(loan_data,data)
            await ctx.message.author.send(f"poopi you messed up big time")
    else:
        await ctx.message.channel.send("You cannot take a loan greater than twice your current balance / you have an unpaid loan, repay it and try again.")

@bot.command(name = "repay-loan", aliases = ["rl"])
async def repay_loan(ctx):
    with open("economy-data.json","r") as data:
        repay_data = json.load(data)
    for i in repay_data:
        if i["user"] == str(ctx.message.author):
            user_data = i
    if user_data["debt"] > 0:
        if user_data["cash"] >= user_data["debt"]:
            user_data["cash"] -= user_data["debt"]
            user_data["debt"] = 0
            with open("economy-data.json","w") as data:
                json.dump(repay_data,data)
            response = discord.Embed(title = str(ctx.message.author), description = f"You've paid off your debt!", colour = discord.Color.green())
            if ctx.message.channel.name in channels_available: await ctx.message.channel.send(content = None, embed = response)
        else:
            if ctx.message.channel.name in channels_available: await ctx.message.channel.send(f"You do not have enough balance to repay your debt.")

    else:
        if ctx.message.channel.name in channels_available: await ctx.message.channel.send(f"You do not have any debt")

@bot.command(name = "inventory", aliases = ["inv"])
async def inventory(ctx, user:discord.Member):
    data_inv,username = ReturnUserDict(user)

    response = discord.Embed(title = username, description = "Inventory")
    for k in data_inv["inv"]:
        response.add_field(name = list(k.keys())[0], value = list(k.values())[0], inline = False)
    
    if ctx.message.channel.name in channels_available: await ctx.message.channel.send(content=None,embed=response)

@inventory.error
async def inventory_error(ctx,error):
    if isinstance(error , commands.errors.MissingRequiredArgument):
        with open("economy-data.json","r") as data:
            data_inv = json.load(data)
    
    for x in data_inv:
            if x["user"] == str(ctx.message.author):
                user_dict = x

    response = discord.Embed(title = f"{str(ctx.message.author)}", description = "Inventory")
    for i in user_dict["inv"]:
        response.add_field(name = list(i.keys())[0],value = list(i.values())[0], inline = False)
    

    if ctx.message.channel.name in channels_available: await ctx.message.channel.send(content=None,embed=response)

@bot.command(name = "shop")
async def shop(ctx):
    with open("store-data.json","r") as data:
        shop_data = json.load(data)
    
    response = discord.Embed(title = f"Shop", description = f"All available items")

    for i in shop_data:
        response.add_field(name = f"""{i["name"]}""", value = f"""Price : {i["price"]} | Remaining Stock : {i["stock"]}""", inline = False )

    if ctx.message.channel.name in channels_available: await ctx.message.channel.send(content = None, embed = response)

@bot.command(name = "buy")                        #IMPORTANT!! - For items that should have unlimited stock, use stock value as None in store-data.json
async def buy(ctx, number:int, item:str):         #pls dont ask me how this code works even i'm not sure anymore...........
    with open("store-data.json","r") as data:
        buy_data_store = json.load(data)
    
    for i in buy_data_store:
        if i["name"].lower() == item.lower():
            item_index = buy_data_store.index(i)
    price_per_item = buy_data_store[item_index]["price"]

    with open("economy-data.json","r") as data:
        buy_data_user = json.load(data)

    for j in buy_data_user:
        if j["user"] == str(ctx.message.author):
            user_index = buy_data_user.index(j)
    
    for k in buy_data_user[user_index]["inv"]:
        if item.lower() in k.keys():
            user_item_details = k
    if buy_data_user[user_index]["cash"] >= (number * price_per_item):
        if buy_data_store[item_index]["stock"] is not None:
            if buy_data_store[item_index]["stock"] >= number:
                buy_data_user[user_index]["cash"] -= (number * price_per_item)
                buy_data_store[item_index]["stock"] -= number
                with open("store-data.json","w") as data:     #updates stock rmeaining in store-data.json
                    json.dump(buy_data_store, data)
                user_item_details[item.lower()] = user_item_details[item.lower()] + number

                with open("economy-data.json","w") as data:
                    json.dump(buy_data_user,data)

                response = discord.Embed(title = str(ctx.message.author), description = f"You bought {number} {item}s!", colour = discord.Color.green())
            
                if ctx.message.channel.name in channels_available: await ctx.message.channel.send(content = None, embed = response)
            else:
                if ctx.message.channel.name in channels_available: await ctx.message.channel.send(f"Bruh not enough stock of this item is left.")
        else:
            buy_data_user[user_index]["cash"] -= (number * price_per_item)
            with open("store-data.json","w") as data:     #updates stock rmeaining in store-data.json
                json.dump(buy_data_store, data)
            user_item_details[item.lower()] = user_item_details[item.lower()] + number

            with open("economy-data.json","w") as data:
                json.dump(buy_data_user,data)

            response = discord.Embed(title = str(ctx.message.author), description = f"You bought {number} {item}s!", colour = discord.Color.green())
            if ctx.message.channel.name in channels_available: await ctx.message.channel.send(content = None, embed = response)
    else:
        if ctx.message.channel.name in channels_available: await ctx.message.channel.send(f"poopi you don't have enough moni {bot.get_emoji(703648812669075456)} ")
    
@bot.command(name = "sell")
async def sell(ctx, n:int, item:str):

    with open("store-data.json","r") as data:
        store = json.load(data)

    for j in store:
        if j["name"].lower() == item.lower():
            price = j["price"]

    with open("economy-data.json","r") as data:
        sell_data = json.load(data)

    for i in sell_data:
        if i["user"] == str(ctx.message.author):
            sell_data_user = i

    for i in sell_data_user["inv"]:
        if item in i.keys():
            item_dict_in_inv = i
    
    item_dict_in_inv[item] = item_dict_in_inv[item] - n

    sell_data_user["cash"] += (price * n)

    with open("economy-data.json","w") as data:
        json.dump(sell_data, data)

    response = discord.Embed(title = f"{str(ctx.message.author)}", description = f"You sold {n} {item}s for {price * n}")

    if ctx.message.channel.name in channels_available: await ctx.message.channel.send(content = None, embed = response)

@bot.command(name='givemoney')
async def givemoney(ctx,person:discord.Member,amount:int):
    with open("economy-data.json","r") as data:
        econ_data = json.load(data)
    
    for i in econ_data:
        if i['user'] == str(ctx.message.author):
            if i['cash'] >= amount:
                i['cash'] -= amount
            else:
                return await ctx.message.channel.send(f"{ctx.message.author.mention} doesn't have enough moni popi barin")
        elif i['user'] == str(person):
            i['user'] += amount

    with open('economy-data.json','w') as data:
        json.dump(econ_data,data)
    
    response = discord.Embed(title='Money Transfer: ', description=f"{ctx.author.mention} transferred {amount} to {person.mention}")
    if ctx.message.channel.name in channels_available: await ctx.message.channel.send(embed=response)

#betting games

@bot.command(name = "roulette")
async def roulette(ctx,amount:int,bet:str):
    with open("economy-data.json","r") as data:
        roulette_user_data = json.load(data)

    for i in roulette_user_data:
        if i["user"] == str(ctx.message.author):
            user_dict = i
            break

    if amount <= user_dict["cash"] and user_dict["cash"] > 0:

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
            user_dict["cash"] -= amount
            with open("economy-data.json","w") as data:
                json.dump(roulette_user_data,data)
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
                    if win_number in list(range(1,13)):
                        user_win = True
                        multiplier = 3
                    else:
                        user_win = False
                elif bet == "13-24":
                    if win_number in list(range(13,25)):
                        user_win = True
                        multiplier = 3
                    else:
                        user_win = False
                elif bet == "25-36":
                    if win_number in list(range(25,37)):
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
                    if win_number in list(range(1,19)):
                        user_win = True
                        multiplier = 2
                else:
                    if win_number in list(range(19,37)):
                        user_win = True
                        multiplier = 2

            elif bet in ["1st", "2nd", "3rd"]:               #columns
                if win_number in roulette_table[bet]:
                    user_win = True
                    multiplier = 3
                
            
        elif int(bet) in list(range(0,37)):
            win_number = random.randint(0,36)
            user_win = False
            user_dict["cash"] -= amount
            with open("economy-data.json","w") as data:
                json.dump(roulette_user_data,data)

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
            with open("economy-data.json", "r") as data:
                roulette_data = json.load(data)
            for i in roulette_data:
                if i["user"] == str(ctx.message.author):
                    i["cash"] += (multiplier * amount)
            with open("economy-data.json","w") as data:
                json.dump(roulette_data, data)
            if ctx.message.channel.name in channels_available: 
                await ctx.message.channel.send(f"The ball fell on {win_number}")
                await ctx.message.channel.send(content = None, embed = response2)
        else:
            response2 = discord.Embed(title = f"Roulette Results {str(ctx.message.author)}", description = f"You lost {amount} {bot.get_emoji(703648812669075456)}", colour = discord.Color.red())
            if ctx.message.channel.name in channels_available: 
                await ctx.message.channel.send(f"The ball fell on {win_number}")
                await ctx.message.channel.send(content = None, embed = response2)
    else:
        await ctx.message.channel.send(f"nigga what you trying? you don't have that much moni")

@bot.command(name = "reverse-russian-roulette", aliases = ["rrr"])
async def russian_roulette(ctx, amount:int):
    response = discord.Embed(title = "Russian Roulette", description = f"{str(ctx.message.author)} started a round of russian roulette for {amount}. Click on the reaction below in the next 15 seconds to join.")
    if ctx.message.channel.name in channels_available: rr_message_init = await ctx.message.channel.send(content = None, embed = response)
    await rr_message_init.add_reaction(bot.get_emoji(703648812669075456))
    await asyncio.sleep(15)
    rr_message = await ctx.message.channel.fetch_message(rr_message_init.id)
    
    users_list = await rr_message.reactions[0].users().flatten()
    users_list.pop(0)
    print(users_list)

    with open("economy-data.json","r") as data:
        rrr_data_full = json.load(data)

    for member in users_list:
        for user_dict in rrr_data_full:
            if user_dict["user"] == str(member):
                if user_dict["cash"] >= amount:
                    print("removed!")
                    user_dict["cash"] -= amount
                elif user_dict["cash"] < amount:
                    users_list.remove(member)

    winner = random.choice(users_list)
    print(users_list, "updated", len(users_list))
    
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
    with open("economy-data.json","w") as data:
        json.dump(rrr_data_full,data)

@bot.command(name = "cock-fight", aliases = ["cf","cockfight"])
async def cockfight(ctx,amount:int):
    with open("economy-data.json","r") as data:
        cf_data = json.load(data)

    win = random.choice([True,False,False,False])
    for i in cf_data:
        if i["user"] == str(ctx.message.author):
            if amount > 0 and amount <= i["cash"]:
                if i["inv"][1]["chicken"] > 0:
                    i["inv"][1]["chicken"] -= 1
                    if win is True:
                        i["cash"] += amount
                        response = discord.Embed(title = str(ctx.message.author), description = f"Your little cock one the fight, making you {amount} richer!", colour = discord.Color.green())
                    else:
                        i["cash"] -= amount
                        response = discord.Embed(title = str(ctx.message.author), description = f"Your cock is weak. It lost the fight.", colour = discord.Color.red())
                else:
                    await ctx.message.channel.send("You don't have enough cocks. Buy one!")
            else:
                await ctx.message.channel.send("Invalid bet.")
    with open("economy-data.json","w") as data:
        json.dump(cf_data,data)
    if ctx.message.channel.name in channels_available: await ctx.message.channel.send(content = None, embed = response)

@bot.command(name = "rob")
async def rob(ctx, person:discord.Member):
    with open("economy-data.json", "r") as data:
        rob_data = json.load(data)
    
    for i in rob_data:
        if i["user"] == str(ctx.message.author):
            robber_dict = i
        elif i["user"] == str(person):
            person_dict = i
    print(f"person - {person_dict} \n robber - {robber_dict}")
    if robber_dict["inv"][2]["heist tools"] > 0 and person_dict["cash"] > 10:
        robber_dict["inv"][2]["heist tools"] -= 1
        
        win_chance = random.choice([True,True,True,False])
        win_percent = random.randint(50,80)
        
        if win_chance is True:
            win_amount = int(person_dict["cash"] * (win_percent/100))
            person_dict["cash"] -= win_amount
            robber_dict["cash"] += win_amount
            print("person-",person_dict, "robber-", robber_dict)
            response = discord.Embed(title = str(ctx.message.author), description = f"You robbed {win_amount} from {str(person)}", colour = discord.Color.green())
            with open("economy-data.json","w") as data:
                json.dump(rob_data,data)
            if ctx.message.channel.name in channels_available: await ctx.message.channel.send(content = None, embed = response)
        else:
            fine_amount = random.randint(75, 200)
            robber_dict["cash"] -= fine_amount
            with open("economy-data.json","w") as data:
                json.dump(rob_data,data)
            response = discord.Embed(title = str(ctx.message.author), description = f"You were caught robbing, and fined {fine_amount}", colour = discord.Color.red())
            if ctx.message.channel.name in channels_available: await ctx.message.channel.send(content = None, embed = response)
    else:
        await ctx.message.channel.send("You do not have enough Heist tools items/ person doesn't have enough cash balance.")
    
#ECONOMY COMMANDS FOR ADMINS AND MODS (REMOVE BOT_DEV ONCE BOT IS DONE)

@bot.command(name="change-money",aliases=["c-money","cm"])                  #gives admins, mods the permission to change money to their own bank (for now)
@commands.has_any_role("Bot Dev","Moderators","admin")                      #this allows multiple roles to have access to one command
async def change_money(ctx,action:str,baltype:str,user:str,amt:int):
    guild = bot.get_guild(298871492924669954)
    members = guild.members
    for i in members:
        if user == i.nick or user == i.name:
            username = str(i)

    with open("economy-data.json","r") as data:
        change_money_data = json.load(data)             
    for i in change_money_data:
        if i["user"] == username:
            user_index = change_money_data.index(i)

    if amt >= 0:
        if action == "add":
            change_money_data[user_index][baltype] = change_money_data[user_index][baltype] + amt
            response = discord.Embed(title = str(ctx.message.author.name), description = f"Added {amt} to {user}\'s {baltype}!" ,colour=discord.Colour.green())
                
        elif action == "remove":
            change_money_data[user_index][baltype] = change_money_data[user_index][baltype] - amt
            response = discord.Embed(title = str(ctx.message.author.name), description = f"Removed {amt} from {user}\'s {baltype}!" ,colour=discord.Colour.red())

        elif action == "set":
            change_money_data[user_index][baltype] = amt
            response = discord.Embed(title = str(ctx.message.author.name), description = f"Set {amt} to {user}\'s {baltype}!" ,colour=discord.Colour.orange()) 

        with open("economy-data.json","w") as data:
            json.dump(change_money_data,data)
        if ctx.message.channel.name in channels_available: await ctx.message.channel.send(content=None,embed=response)

@bot.command(name = "change-stock")
@commands.has_any_role("Moderators","admin","Bot Dev")
async def change_stock(ctx, item:str, n:int):
    with open("store-data.json","r") as data:
        store_data = json.load(data)
    print(store_data)
    
    for i in store_data:
        if i["name"].lower() == item.lower():
            i["stock"] = n

    with open("store-data.json","w") as data:
        json.dump(store_data,data)

    response = discord.Embed(title = str(ctx.message.author.name), description = f"Updated stock of {item}")
    if ctx.message.channel.name in channels_available: await ctx.message.channel.send(content = None, embed = response)
@bot.command(name = "remove-user")
@commands.has_any_role("Moderators","admin","Bot Dev")
async def remove_user(member):
    with open("economy-data.json","r") as data:
        remove_user_data = json.load(data)
    for i in remove_user_data:
        if i["user"] == str(member):
            remove_user_data.remove(i)
            break

    with open("economy-data.json","w") as data:
        json.dump(remove_user_data, data)
    await member.send(f"haha popi you got deleted from the bot database")
    
@bot.command(name = "change-inventory",aliases=["c-inv"])
@commands.has_any_role("Moderators","admin","Bot Dev")
async def change_inventory(ctx,action:str,amt:int,item:str,user:str):
    guild = bot.get_guild(298871492924669954)
    members = guild.members
    for i in members:
        if user == i.nick or user == i.name:
            username = str(i)

    with open("economy-data.json","r") as data:
        data_inv = json.load(data)

    for i in data_inv:
        if i["user"] == username:
            user_index = data_inv.index(i)
    
    if action == "add":
        for i in data_inv[user_index]["inv"]:
            if item in i.keys():
                i[item] = i[item] + amt
                response = discord.Embed(title = str(ctx.message.author.name), description = f"Added {amt} {item}(s) to {user}\'s inventory!",colour=discord.Colour.green())
             
    elif action == "remove":
        for i in data_inv[user_index]["inv"]:
            if item in i.keys():
                i[item] = i[item] - amt
                response = discord.Embed(title = str(ctx.message.author.name), description = f"Removed {amt} {item}(s) from {user}\'s inventory!",colour=discord.Colour.red())

    elif action == "set":
        for i in data_inv[user_index]["inv"]:
            if item in i.keys():
                i[item] = amt
                response = discord.Embed(title = str(ctx.message.author.name), description = f"Set {amt} {item}(s) to {user}\'s inventory!",colour=discord.Colour.orange())
        

    with open("economy-data.json","w") as data:
        json.dump(data_inv,data)
    
    if ctx.message.channel.name in channels_available: await ctx.message.channel.send(content = None, embed = response)

#--------------------RPG / HORO FUNCTIONS----------------------
#global variables
battle_ongoing = False
turn_count = 1

@bot.command(name='horo-assign')
async def assign_horoscope(ctx):
    msg = await ask_date(ctx)
    sign = get_zodiac(msg)
    update_json_database(msg,sign)
    response = discord.Embed(title='Horoscope',description=f'Congratulations! You are a {sign}')
    await ctx.message.channel.send(embed=response)
    
async def ask_date(ctx):
    def check(author):
        def inner_check(message):
            if message.author != author:
                return False
            try:
                int(message.content)
                return True
            except ValueError:
                return False
        return inner_check
    response = discord.Embed(title='Horoscope',description='Please enter your date of birth: ')
    await ctx.message.channel.send(embed=response)
    return await bot.wait_for('message',check=check)

def check_date(jsondata, authordata):         #Is called inside ask_date()
    date = authordata.content.split('-')
    days = [31,28,31,30,31,30,31,31,30,31,30,31]
    sum_ = 0                               #renamed sum to sum_ to retain sum functionality
    for i in range(int(date[1])-1):
        sum_+=days[i]
    sum_+=int(date[0])
    if 0<sum_<19:sum_+=366
    if jsondata["day_low"]<=sum_<=jsondata["day_high"]: return True

def get_zodiac(response):
    data = open("horo-data.json","r")
    data_horo = json.load(data)
    for i in data_horo:
        if check_date(i,response): 
            zodiac = i["Zodiac"]
            data.close()
            return zodiac

def update_json_database(response,sign):
    data = open("rpg-data.json","r")
    rpg_data = json.loads(data.readline())
    data.close()

    for i in rpg_data:
        if i["user"] == str(response.author):
            user_index = rpg_data.index(i)

    rpg_data[user_index]["zodiac_sign"] = sign
    with open("rpg-data.json","w") as data:
        json.dump(rpg_data,data)


@bot.command(name='battle')
async def battle(ctx,person:discord.Member,bet:int):
    if person != ctx.author:
        if battle_ongoing == False:
            battle_state, contestant_data, stats, battle_status = await begin_battle(ctx,person,ctx.message.author,bet)
        if battle_state == True:
            await process_battle(battle_state,ctx,contestant_data,stats,battle_status)
            await end_battle(ctx,contestant_data,bet)
            
    else:
        response = discord.Embed(title='Error',description='Another battle is ongoing. Please wait.')
        await ctx.message.channel.send(embed=response)
    
#Battle beginning    
async def begin_battle(ctx,person,author,bet):
    await send_challenge(ctx,person,author,bet)
    reply = await get_reply(ctx,person)
    battle_state = await check_reply(ctx,person,author,reply.content,bet)
    if battle_state:
        contestant_data = get_contestant_data(person,author)
        #deduct_from_balance(person,author,bet,contestant_data)
        stats, battle_status = await display_beginning_stats(ctx,person,author,contestant_data)
        return battle_state, contestant_data, stats, battle_status
    return battle_state,None,None,None
    

#Sub Functions of Begin Battle:

async def send_challenge(ctx,person,author,bet):
    response = discord.Embed(title='Battle', description=f'{author.mention} challenges {person.mention} to a battle \n\n {person.mention} do you accept?')
    response.add_field(name='Bet', value=str(bet)+" + 5% of your balance if you win")
    await ctx.message.channel.send(embed=response)

async def get_reply(ctx,person):
    def check(m): 
        nonlocal person
        if m.content in ['yes','no'] and m.author == person:
            return True

    return await bot.wait_for('message',check=check)

async def check_reply(ctx,person,author,reply,bet):
    if reply == 'yes':
        response = discord.Embed(title='Battle', description=f'{person.mention} has accepted the challenge')
        response.add_field(name='Challenger', value=author.name)
        response.add_field(name='Challengee', value=person.name)
        response.add_field(name='Winner\'s Prize: ', value=str(2*bet)+' + 5% winner\'s balance')
        global battle_ongoing
        battle_ongoing = True
        return True
        
    elif reply == 'no':
        response = discord.Embed(title='Battle', description=f'{person.mention} has declined the challenge')
        await ctx.channel.send(embed = response)
        return False
    
def get_contestant_data(person,author):
    data = open("rpg-data.json","r")
    data_rpg = json.load(data)
    data.close()
    for i in data_rpg:
        if i['user'] == str(author):
            author_data = i
            author_index = data_rpg.index(i)
        if i['user'] == str(person):
            person_data = i
            person_index = data_rpg.index(i)
    return [author_data,person_data,author_index,person_index]
    
def deduct_from_balance(person,author,bet,contestant_data):
    data = open('economy-data.json','r')
    econ_data = json.load(data)
    data.close()
    if econ_data[contestant_data[2]]['cash'] >= bet and econ_data[contestant_data[3]]['cash'] >= bet:
        econ_data[contestant_data[2]]['cash'] -= bet
        econ_data[contestant_data[3]]['cash'] -= bet
        with open('economy-data.json','w') as data:
            json.dump(econ_data,data)


async def display_beginning_stats(ctx,person,author,contestant_data):
    stats_beginning = make_stats_embed(contestant_data)

    starter = discord.Embed(title='The Battle Begins!')

    stats = await ctx.channel.send(embed=stats_beginning)
    battle_status = await ctx.channel.send(embed=starter)

    return stats, battle_status

def make_stats_embed(contestant_data): #Used in process battle too
    author_data = contestant_data[0]
    person_data = contestant_data[1]

    stats_beginning = discord.Embed(title='Battle: Stats')
    stats_beginning.add_field(name='|',value='|')
    stats_beginning.add_field(name=author_data['user'], value=author_data['zodiac_sign'])
    stats_beginning.add_field(name=person_data['user'], value=person_data['zodiac_sign'])
    stats_beginning.add_field(name='|',value='|')
    stats_beginning.add_field(name='Health', value=author_data['hp'])
    stats_beginning.add_field(name='Health', value=person_data['hp'])
    stats_beginning.add_field(name='|',value='|')
    stats_beginning.add_field(name='Attack', value=author_data['attack'])
    stats_beginning.add_field(name='Attack', value=person_data['attack'])
    stats_beginning.add_field(name='|',value='|')
    stats_beginning.add_field(name='Defense', value=author_data['defense'])
    stats_beginning.add_field(name='Defense', value=person_data['defense'])

    return stats_beginning

#Battle Process
async def process_battle(battle_state,ctx,contestant_data,stats,battle_status):
    player_1 = 0
    player_2 = 0
    global turn_count
    while battle_state:
        if turn_count == 1:player_1, player_2, player_turn = await get_turn(ctx,contestant_data,player_1,player_2)
        if turn_count == 1:action, player_choice = await get_player_choice(ctx,contestant_data,player_1)
        else: action = await get_player_choice(ctx,contestant_data,player_1)
        battle_status_response = await process_action(ctx,contestant_data,player_1,player_2,action.content)
        player_1, player_2 = await update_battle(ctx,contestant_data,player_1,player_2,stats,battle_status,player_turn,player_choice,battle_status_response,action)
        if contestant_data[0]['hp']<=0 or contestant_data[1]['hp']<=0:
            await asyncio.sleep(2)
            await stats.delete()
            await battle_status.delete()
            await player_turn.delete()
            await player_choice.delete()
            battle_state=False
        
    
#Sub Functions of Process Battle:

async def get_turn(ctx,contestant_data,player_1=0,player_2=0):
    global turn_count
    if turn_count == 1: 
        player_1 = choice([0,1])
        if player_1 == 0: player_2 = 1
        else: player_2 = 0
    response = discord.Embed(title=f'Turn {turn_count}: ',description=f"{contestant_data[player_1]['user']}'s Turn")
    player_turn = await ctx.channel.send(embed=response)
    return player_1, player_2, player_turn
    
async def get_player_choice(ctx,contestant_data,player_1):
    global turn_count

    def check(m):
        if str(m.author) == contestant_data[player_1]['user'] and m.content in contestant_data[player_1]['battle_options']: return True

    if turn_count == 1:
        response = discord.Embed(title='Player Choice',description=f''' {contestant_data[player_1]['user']}, What would you like to do?\n{contestant_data[player_1]['battle_options']}''')
        player_choice = await ctx.channel.send(embed=response)
        return await bot.wait_for('message',check=check), player_choice
    return await bot.wait_for('message',check=check)

async def process_action(ctx,contestant_data,player_1,player_2,action):
    if action == 'attack': battle_status_response = await process_attack(ctx,contestant_data,player_1,player_2)
    elif action == 'defend': battle_status_response = await process_defense(ctx,contestant_data,player_1)
    #elif action == 'use item': await process_use_item(ctx,contestant_data,player_1,player_2)  Will implement once items are made
    return battle_status_response

async def update_battle(ctx,contestant_data,player_1,player_2,stats,battle_status,player_turn,player_choice,battle_status_response,action):
    global turn_count
    turn_count+=1
    update_statuses(contestant_data,player_1,player_2)

    new_stats = make_stats_embed(contestant_data)
    new_battle_status = discord.Embed(title='Battle Status:',description=f"{battle_status_response.description}\n{contestant_data[player_1]['user']}'s turn has ended'")
    
    
    player_1, player_2 = player_2, player_1
  

    new_player_turn = discord.Embed(title=f'Turn {turn_count}: ',description=f"{contestant_data[player_1]['user']}'s Turn")
    new_player_choice = discord.Embed(title='Player Choice',description=f''' {contestant_data[player_1]['user']}, What would you like to do?\n{contestant_data[player_1]['battle_options']}''')

    await stats.edit(embed=new_stats)
    await battle_status.edit(embed=new_battle_status)
    await player_turn.edit(embed=new_player_turn)
    await player_choice.edit(embed=new_player_choice)
    await action.delete()
    return player_1, player_2

#Sub functions of update battle:
def update_statuses(contestant_data,player_1,player_2):

    for i in contestant_data[0:1]:
        for j in i['battle_counters']:
            if i['battle_counters'][j][0] >=1:
                i['battle_counters'][j][0]-=1
                if i['battle_counters'][j][0]==0:
                    i[j] -= i['battle_counters'][j][1]

#Sub functions of process action:
async def process_attack(ctx,contestant_data,player_1,player_2):
    damage = contestant_data[player_1]['attack'] - contestant_data[player_2]['defense']//10 + choice([-3,-2,-1,0,1,2,3])
    contestant_data[player_2]['hp'] -= damage
    battle_status_response = discord.Embed(title='Battle Status:',description=f"{contestant_data[player_1]['user']} dealt {damage} damage to the opposing player!")
    return battle_status_response
    
async def process_defense(ctx,contestant_data,player_1):
    contestant_data[player_1]['battle_counters']['defense']=[2,40]
    contestant_data[player_1]['defense'] += 40
    battle_status_response = discord.Embed(title='Battle Status:',description=f"{contestant_data[player_1]['user']} defended!")
    return battle_status_response

#End Battle
async def end_battle(ctx,contestant_data,bet):
    global battle_ongoing
    battle_ongoing = False
    if contestant_data[0]['hp'] == 0:
        winner = contestant_data[2]
    else: winner = contestant_data[3]
    data = open('economy-data.json','r')
    econ_data = json.load(data)
    data.close()
    amt = int(2*bet + 0.05*econ_data[winner]['cash'])
    econ_data[winner]['bal'] += amt
    response = discord.Embed(title=f"{econ_data[winner]['user']} wins!",
    description=f"{econ_data[winner]['user']} wins {amt}")
    with open('economy-data.json','w') as data:
        json.dump(econ_data,data)

    await ctx.channel.send(embed=response)

#TESTING AUTO PRICE CHANGE OF STOCK
@tasks.loop(seconds =  10800)
async def stock_price():
    with open("store-data.json","r") as data:
        stock_data = json.load(data)
    new_price = random.randint(stock_data[0]["price"] - 5, stock_data[0]["price"] + 5)
    stock_data[0]["price"] = new_price
    with open("store-data.json","w+") as data:
        json.dump(stock_data,data)
    await message_channel.send(f"Stock price : {new_price}")

@stock_price.before_loop
async def stock_price_before():
    global message_channel
    await bot.wait_until_ready()
    message_channel = bot.get_channel(704911379341115433)
    

stock_price.start()
bot.run(token)