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

#bot token stuff; not to be messed with :linus_gun:
token_ = "NzA5NDA3MjY4NDg3MDM3MDE5.XrllLQ.FbL2vivvNxjxPT-wOfAvH32fK4QZ"
token = token_[:len(token_)-1]

#bot which controls everything; subclass of Client
bot = commands.Bot(command_prefix='$')

channels_available = ["bot-test","botspam-v2","botspam"] #Channels where the bot works
bot.remove_command('help') 
#Lets us implement our own help command instead of the built in one

@bot.event
async def on_ready(): #sends this message when bot starts working in #bot-tests
    await bot.get_channel(703141348131471440).send("its popi time")
    

#ctx stands for context

@bot.command(name='popi')
async def popi(ctx):
    reply = random.choice(["poopi really do be poopie though",f"{ctx.message.author.mention} is a poopie?oh no......"]) #Choice chooses 1 object from the list
    response = discord.Embed(title='popi',description=reply)
    if ctx.message.channel.name in channels_available: await ctx.message.channel.send(content=None,embed=response)

@bot.command(name='help')
async def help(ctx):
    response = discord.Embed(title='Help',description='List of commands')
    response.add_field(name="$popi", value="popi", inline = False)
    response.add_field(name="Some economy function:", value = "----------", inline = False)
    response.add_field(name="$bal", value="Displays balance in Bank, Debt and Net Worth", inline = False)
    response.add_field(name="$work", value="You work, lazy popi", inline = False)
    response.add_field(name="$slut", value="hoe life", inline = False)
    response.add_field(name="$crime", value="gangsta tiem", inline = False)
    response.add_field(name="$get-loan", value="You take out a loan of specified amount. Max amount of loan is twice your current balance. 5% interest applies on the loan (one time only,if you pay before 1 day after loan request you have to pay 5% interest as well). If you do not repay loan in 1 day, bot will auto deduct 10% extra from your balance.", inline = False)
    response.add_field(name="$repay-loan", value="Repay your existing debts.", inline = False)
    response.add_field(name="$inv", value="Checks inventory", inline = False)
    response.add_field(name="$shop", value="Check shop", inline = False)
    response.add_field(name=f"$buy <number> <item>", value="Buys item from store. No need to use those brackets", inline = False)
    response.add_field(name=f"$sell <number> <item>", value="Sell item back to shop for current market price", inline = False)
    response.add_field(name="$roulette", value="you know how this works", inline = False)
    if ctx.message.channel in channels_available: await ctx.message.channel.send(content = None, embed = response)
#ECONOMY CODE; ADD SPACE ABOVE THIS FOR OTHER UNRELATED FUNCTIONS PLEASE :linus_gun:

@bot.command(name='bal')
async def balance(ctx,user:str):
    global guild
    global members
    guild = bot.get_guild(298871492924669954)
    members = guild.members

    for i in members:
        if user == i.nick or user == i.name:
            username = str(i)

    with open("economy-data.json","r") as data:
        data_bal = json.load(data)


    for x in data_bal:
        if x["user"] == username:
            user_dict = x                 #gets right dictionary with all user vals from a list of dicts.
    
    networth = user_dict["bal"] - user_dict["debt"]
    
    response = discord.Embed(title=username, description="Balance is:")
    response.add_field(name="Bank balance : ",value=f"{user_dict['bal']}", inline = False)
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

        networth = user_dict["bal"] - user_dict["debt"]

        response = discord.Embed(title=str(ctx.message.author), description="Your balance is:")
        response.add_field(name="Bank balance : ",value=f"{user_dict['bal']}", inline = False)
        response.add_field(name="Debt : ",value=f"{user_dict['debt'] * (-1)}", inline = False)
        response.add_field(name="Net Worth : ",value=networth, inline = False)

        if ctx.message.channel.name in channels_available: await ctx.message.channel.send(content=None,embed=response)

@bot.command(name='work')
@commands.cooldown(1, 60, commands.BucketType.user)            #remember to increase the cooldown to at least an hour!
async def work(ctx):
        data = open("economy-data.json","r")
        data_bal = json.loads(data.readline())
        data.close()
        for i in data_bal:
            if i["user"] == str(ctx.message.author):
                user_index = data_bal.index(i)
        

        rand_val = random.randint(35,150)
        data_bal[user_index]["bal"] = data_bal[user_index]["bal"] + rand_val
        data = open("economy-data.json","w")
        json.dump(data_bal,data)    #changing value in main json file as well
        data.close()

        response = discord.Embed(title=str(ctx.message.author),description=f"You earned {rand_val}",colour=discord.Colour.green())

    
        if ctx.message.channel.name in channels_available: await ctx.message.channel.send(content=None,embed=response)

@bot.command(name='slut')
@commands.cooldown(1, 60, commands.BucketType.user)            #remember to increase the cooldown to at least an hour!
async def slut(ctx):
    with open("economy-data.json","r") as data:
        data_bal = json.load(data)
    for i in data_bal:
        if i["user"] == str(ctx.message.author):
            user_index = data_bal.index(i)

    winning_odds=[1,2,3,4,5,6]
    if random.randint(1,10) in winning_odds:
        rand_val = random.randint(60,300)
        data_bal[user_index]["bal"] = data_bal[user_index]["bal"] + rand_val
        response = discord.Embed(title=str(ctx.message.author),description=f"You whored out and earned {rand_val}!",colour=discord.Colour.green())
    
    else:
        rand_val = random.randint(60,300)
        data_bal[user_index]["bal"] = data_bal[user_index]["bal"] - rand_val
        response = discord.Embed(title=str(ctx.message.author),description=f"You hooked up with a psychopath lost {rand_val}!",colour=discord.Colour.red())

    with open("economy-data.json","w") as data:
        json.dump(data_bal,data)

    if ctx.message.channel.name in channels_available: await ctx.message.channel.send(content=None,embed=response)

@bot.command(name="crime")
@commands.cooldown(1, 60, commands.BucketType.user)            #remember to increase the cooldown to at least an hour!
async def crime(ctx):
    with open("economy-data.json","r") as data:
        data_bal = json.load(data)
    for i in data_bal:
        if i["user"] == str(ctx.message.author):
            user_index = data_bal.index(i)

    winning_odds=[1,2,3,4]
    if random.randint(1,10) in winning_odds:
        rand_val = random.randint(150,750)
        data_bal[user_index]["bal"] = data_bal[user_index]["bal"] + rand_val
        response = discord.Embed(title=str(ctx.message.author),description=f"You successfuly commited crime and earned {rand_val}!",colour=discord.Colour.green())
    
    else:
        rand_val = random.randint(150,750)
        data_bal[user_index]["bal"] = data_bal[user_index]["bal"] - rand_val
        response = discord.Embed(title=str(ctx.message.author),description=f"You you got caught and were fined {rand_val}!",colour=discord.Colour.red())

    with open("economy-data.json","w") as data:
        json.dump(data_bal,data)

    if ctx.message.channel.name in channels_available: await ctx.message.channel.send(content=None,embed=response)

@bot.command(name="get-loan", aliases = ["gl"])    #beta loan command! repayment not yet made
async def loan(ctx,loan_val:int):
    
    with open("economy-data.json","r") as data:
        loan_data = json.load(data)
    for i in loan_data:
        if i["user"] == str(ctx.message.author):
            user_index = loan_data.index(i)
    if loan_val < loan_data[user_index]["bal"] * 2 and loan_data[user_index]["debt"] == 0:
        response = discord.Embed(title=str(ctx.message.author),description=f"You took a loan of {loan_val}!",colour=discord.Colour.red()) # red bc u did a dum dum

        loan_data[user_index]["debt"] = loan_data[user_index]["debt"] + (loan_val + int(loan_val * 0.05))
        loan_data[user_index]["bal"] = loan_data[user_index]["bal"] + loan_val
        
        with open("economy-data.json","w") as data:
            json.dump(loan_data,data)
        if ctx.message.channel.name in channels_available: await ctx.message.channel.send(content=None,embed=response)
        await asyncio.sleep(64800)
        await ctx.message.author.send("You're about to default on your loan")
        await asyncio.sleep(21600)

        with open("economy-data.json","r") as data:
            loan_data = json.load(data)
        for i in loan_data:
            if i["user"] == str(ctx.message.author):
                user_index = loan_data.index(i)
        if loan_data[user_index]["debt"] != 0:
            loan_data[user_index]["debt"] = 0
            loan_data[user_index]["bal"] = loan_data[user_index]["bal"] - (loan_val + int(loan_val * 0.1))
            with open("economy-data.json","w") as data:
                json.dump(loan_data,data)
            await ctx.message.author.send(f"poopi you messed up big time")
    else:
        await ctx.message.channel.send("You cannot take a loan greater than twice your current balance / you have an unpaid loan, repay it and try again.")


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

@bot.command(name = "inventory", aliases = ["inv"])
async def inventory(ctx, user:str):
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

    response = discord.Embed(title = username, description = "Inventory")
    response.add_field(name = "Stock", value = data_inv[user_index]["inv"][0]["stock"], inline = False)
    
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
    response.add_field(name = "Stock", value = user_dict["inv"][0]["stock"], inline  = False)

    if ctx.message.channel.name in channels_available: await ctx.message.channel.send(content=None,embed=response)

@bot.command(name = "shop")
async def shop(ctx):
    with open("store-data.json","r") as data:
        shop_data = json.load(data)
    
    response = discord.Embed(title = f"Shop", description = f"All available items")
    response.add_field(name = f"Stock", value = f"""Price : {shop_data[0]["price"]} | Remaining Stock : {shop_data[0]["stock"]}""" )

    if ctx.message.channel.name in channels_available: await ctx.message.channel.send(content = None, embed = response)

@bot.command(name = "buy")
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
    if buy_data_user[user_index]["bal"] >= (number * price_per_item):
        if buy_data_store[item_index]["stock"] >= number:
            buy_data_user[user_index]["bal"] = buy_data_user[user_index]["bal"] - (number * price_per_item)
            buy_data_store[item_index]["stock"] = buy_data_store[item_index]["stock"] - number
            with open("store-data.json","w") as data:     #updates stock rmeaining in store-data.json
                json.dump(buy_data_store, data)
            user_item_details[item] = user_item_details[item] + number

            with open("economy-data.json","w") as data:
                json.dump(buy_data_user,data)

            response = discord.Embed(title = str(ctx.message.author), description = f"You bought {number} {item}s!", colour = discord.Color.green())
        
            if ctx.message.channel.name in channels_available: await ctx.message.channel.send(content = None, embed = response)
        else:
            if ctx.message.channel.name in channels_available: await ctx.message.channel.send(f"Bruh not enough stock of this item is left.")
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

    sell_data_user["bal"] = sell_data_user["bal"] + (price * n)

    with open("economy-data.json","w") as data:
        json.dump(sell_data, data)

    response = discord.Embed(title = f"{str(ctx.message.author)}", description = f"You sold {n} {item}s for {price * n}")

    if ctx.message.channel.name in channels_available: await ctx.message.channel.send(content = None, embed = response)

@bot.command(name = "roulette")
async def roulette(ctx,amount:int,bet:str):
    with open("economy-data.json","r") as data:
        roulette_user_data = json.load(data)

    for i in roulette_user_data:
        if i["user"] == str(ctx.message.author):
            user_bal = i["bal"]

    if amount < user_bal and user_bal > 0:
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
                        multiplier = 3
                elif bet == "odd":
                    if win_number % 2 != 0:
                        user_win = True
                        multiplier = 3

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
                    i["bal"] = i["bal"] + (multiplier * amount)
            with open("economy-data.json","w") as data:
                json.dump(roulette_data, data)
            if ctx.message.channel.name in channels_available: 
                await ctx.message.channel.send(f"The ball fell on {win_number}")
                await ctx.message.channel.send(content = None, embed = response2)
        else:
            response2 = discord.Embed(title = f"Roulette Results {str(ctx.message.author)}", description = f"You lost {amount} {bot.get_emoji(703648812669075456)}", colour = discord.Color.red())
            with open("economy-data.json", "r") as data:
                roulette_data = json.load(data)
            for i in roulette_data:
                if i["user"] == str(ctx.message.author):
                    i["bal"] = i["bal"] - amount
            with open("economy-data.json","w") as data:
                json.dump(roulette_data, data)
            if ctx.message.channel.name in channels_available: 
                await ctx.message.channel.send(f"The ball fell on {win_number}")
                await ctx.message.channel.send(content = None, embed = response2)
    else:
        await ctx.message.channel.send(f"nigga what you trying? you don't have that much moni")

#ECONOMY COMMANDS FOR ADMINS AND MODS (REMOVE BOT_DEV ONCE BOT IS DONE)

@bot.command(name="change-money",aliases=["c-money","cm"])                  #gives admins, mods the permission to change money to their own bank (for now)
@commands.has_any_role("Bot Dev","Moderators","admin")                      #this allows multiple roles to have access to one command
async def change_money(ctx,action:str,amt:int,user:str):
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

    if amt > 0:
        if action == "add":
            change_money_data[user_index]["bal"] = change_money_data[user_index]["bal"] + amt
            response = discord.Embed(title = str(ctx.message.author.name), description = f"Added {amt} to {user}\'s bank!" ,colour=discord.Colour.green())
                
        elif action == "remove":
            change_money_data[user_index]["bal"] = change_money_data[user_index]["bal"] - amt
            response = discord.Embed(title = str(ctx.message.author.name), description = f"Removed {amt} from {user}\'s bank!" ,colour=discord.Colour.red())

        elif action == "set":
            change_money_data[user_index]["bal"] = amt
            response = discord.Embed(title = str(ctx.message.author.name), description = f"Set {amt} to {user}\'s bank!" ,colour=discord.Colour.orange()) 

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
        data_inv[user_index]["inv"][0][item] = data_inv[user_index]["inv"][0][item] + amt
        response = discord.Embed(title = str(ctx.message.author.name), description = f"Added {amt} {item}(s) to {user}\'s inventory!",colour=discord.Colour.green())
             
    elif action == "remove":
        data_inv[user_index]["inv"][0][item] = data_inv[user_index]["inv"][0][item] - amt
        response = discord.Embed(title = str(ctx.message.author.name), description = f"Removed {amt} {item}(s) from {user}\'s inventory!",colour=discord.Colour.red())

    elif action == "set":
        data_inv[user_index]["inv"][0][item] = amt
        response = discord.Embed(title = str(ctx.message.author.name), description = f"Set {amt} {item}(s) to {user}\'s inventory!",colour=discord.Colour.orange())
        

    with open("economy-data.json","w") as data:
        json.dump(data_inv,data)
    
    if ctx.message.channel.name in channels_available: await ctx.message.channel.send(content = None, embed = response)

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

